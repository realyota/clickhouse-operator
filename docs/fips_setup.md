# FIPS-compatible deployment example

This document presents a reference deployment of the ClickHouse Operator in a
FIPS-compatible posture: FIPS-built images, secure ports only, and verified TLS
between every component. It walks through the four example manifests that make
up the deployment and highlights the main FIPS-related option in each. The
cryptographic-module gate, image policy, and release evidence are covered in
[`security_hardening_fips.md`](./security_hardening_fips.md); the general TLS
knobs and certificate setup are covered in
[`security_hardening.md`](./security_hardening.md).

## Limitations

The FIPS boundary covers the operator and metrics-exporter binaries only, so a
few paths stay outside it. The operator-to-metrics-exporter IPC and the
Prometheus metrics endpoints (operator `:9999`, metrics-exporter
`:8888/metrics`) remain plain HTTP. TLS is server-authentication only, not
mutual TLS, because the operator has no client-certificate settings for its
health and version connections to ClickHouse.

## Order of apply

Apply the manifests in this order:

1. [`25-fips-01-chopconf.yaml`](chi-examples/25-fips-01-chopconf.yaml) — operator
   configuration.
2. The `clickhouse-certs` Secret — the shared TLS material; see
   [`security_hardening.md`](./security_hardening.md#certificates-and-ca-trust).
3. [`31-fips-secure-cluster.yaml`](chk-examples/31-fips-secure-cluster.yaml) —
   Keeper cluster.
4. [`25-fips-02-cluster.yaml`](chi-examples/25-fips-02-cluster.yaml) and
   [`107-fips-backup-sidecar.yaml`](chit-examples/107-fips-backup-sidecar.yaml) —
   ClickHouse cluster and its backup template.

The backup template (CHIT) must exist before or alongside the ClickHouse
cluster, which pulls it in through `useTemplates`.

## Operator configuration

[`25-fips-01-chopconf.yaml`](chi-examples/25-fips-01-chopconf.yaml) turns on the
operator's FIPS posture. Setting `policy: Enforced` and `fips.enforced: true`
makes the operator coerce every outbound TLS connection to verified mode and
assert at startup that its binary is linked against the Go FIPS module.

```yaml
spec:
  security:
    policy: Enforced
    fips:
      enforced: "true"
```

## ClickHouse cluster

[`25-fips-02-cluster.yaml`](chi-examples/25-fips-02-cluster.yaml) runs ClickHouse
on secure ports only. The plain-text ports are removed and replaced by their TLS
equivalents, and the cluster trusts the shared CA through `rootCASecretRef`.

```yaml
settings:
  http_port: _removed_
  tcp_port: _removed_
  interserver_http_port: _removed_
  mysql_port: _removed_
  postgresql_port: _removed_
  https_port: 8443
  tcp_port_secure: 9440
  interserver_https_port: 9010
```

The `openssl.xml` file pins both the server and client to 1.3 and a
FIPS-approved cipher suite. The server presents its certificate without
requesting one from clients (`verificationMode: none`), while the client side
validates the server against the mounted CA in strict mode.

```xml
<client>
  <caConfig>/etc/clickhouse-server/secrets.d/ca.crt/clickhouse-certs/ca.crt</caConfig>
  <loadDefaultCAFile>false</loadDefaultCAFile>
  <verificationMode>strict</verificationMode>
  <disableProtocols>sslv2,sslv3,tlsv1,tlsv1_1</disableProtocols>
  <cipherSuites>TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384</cipherSuites>
</client>
```

## Keeper cluster

[`31-fips-secure-cluster.yaml`](chk-examples/31-fips-secure-cluster.yaml) runs
ClickHouse Keeper on a FIPS-built image with TLS-only ports. Setting
`secure: "yes"` and `insecure: "no"` drops the plain-text client port 2181,
opens the secure client port 2281, and secures the Raft traffic between Keeper nodes.

```yaml
clusters:
  - name: keeper
    secure: "yes"
    insecure: "no"
settings:
  keeper_server/raft_configuration/server/port: 9444
```

Keeper uses the same `openssl.xml` server and client blocks as ClickHouse and
pulls its image from `altinity/clickhouse-keeper:<ver>.altinityfips`.

## Backup sidecar

[`107-fips-backup-sidecar.yaml`](chit-examples/107-fips-backup-sidecar.yaml) is
the template that supplies the FIPS-built ClickHouse and clickhouse-backup
images. The backup container serves its API over HTTPS and connects to
ClickHouse over the secure native port with CA verification enabled.

```yaml
- name: CLICKHOUSE_SECURE
  value: "true"
- name: CLICKHOUSE_TLS_CA
  value: /etc/clickhouse-backup/tls/ca.crt
- name: CLICKHOUSE_SKIP_VERIFY
  value: "false"
```

It mounts the same `clickhouse-certs` Secret used by the rest of the deployment.

## Related

- FIPS controls, GODEBUG, image policy, and release evidence:
  [`security_hardening_fips.md`](./security_hardening_fips.md).
- TLS knobs, coercion, and certificate setup:
  [`security_hardening.md`](./security_hardening.md).
- Per-release verification recipes:
  [`fips_evidence_verification.md`](./fips_evidence_verification.md).
