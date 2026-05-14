# Security hardening

This document describes the per-component security toggles introduced in 0.27.1+.
The toggles are opt-in: with no configuration changes the operator behaves
exactly as in 0.26.x.

Each toggle is independent — the operator does not infer one knob from another.
This lets users harden one surface (e.g. ClickHouse client TLS) without
disturbing others.

## What is configurable

| Surface | Knob | Default | Strict value |
|---|---|---|---|
| ClickHouse client TLS | `verify` | (legacy `InsecureSkipVerify=true`) | `Strict` |
| ClickHouse client TLS | `minVersion` | Go default (1.2) | `"1.3"` |
| ClickHouse client TLS | `serverName` | derived from dial host | explicit |
| ClickHouse client TLS | `rootCA` | from chopconf `access.rootCA` | (unchanged; per-cluster override available) |
| ZooKeeper / Keeper TLS | `verify` | strict (RootCAs+ServerName always set) | `Strict` |
| ZooKeeper / Keeper TLS | `minVersion` | Go default | `"1.3"` |
| Kubernetes client (chopconf only) | `tls.verify` | (unset; kubeconfig wins) | `Strict` |
| Kubernetes client (chopconf only) | `tls.minVersion` | (unset; declared but not yet wired to K8s transport) | `"1.3"` |
| Operator↔exporter IPC | `mode` | `Plain` | `Secure` |
| Operator↔exporter IPC | `bindHost` | (Plain: all interfaces) | `127.0.0.1` |

## Where toggles live

Toggles surface at two levels with 3-level inheritance (CHOP-config → CHI spec
→ cluster spec). Lower level wins; empty fields fall through.

### Operator-wide (chopconf — `ClickHouseOperatorConfiguration` CR)

```yaml
spec:
  security:
    clickhouse:
      tls:
        verify: Strict
        minVersion: "1.2"
    zookeeper:
      tls:
        minVersion: "1.2"
    kubernetes:
      tls:
        verify: Strict
    ipc:
      mode: Secure
```

**Location note**: `security:` lives at the top level of the chopconf spec —
sibling of `spec.clickhouse`, not under it. The block covers more than ClickHouse
(ZooKeeper TLS, Kubernetes client posture, operator-internal IPC, operator-wide
FIPS), so nesting it under `clickhouse` would be misleading.

### Per-CHI (ClickHouseInstallation CR — `spec.configuration.clusters[].security`)

```yaml
spec:
  configuration:
    clusters:
      - name: prod
        security:
          clickhouse:
            tls:
              verify: Strict
              rootCA: |
                -----BEGIN CERTIFICATE-----
                ...
                -----END CERTIFICATE-----
```

The CHI block does NOT contain `ipc` or `kubernetes` — IPC is between the
operator and the metrics-exporter sidecar (both in the operator's own Pod),
and the Kubernetes API client is operator-process-scoped (one kubeconfig per
operator pod). Both are configurable in ClickHouseOperatorConfiguration only.

## How each toggle works

### `security.clickhouse.tls.verify`

Controls peer-certificate + hostname verification on outbound TLS connections
the operator makes to ClickHouse hosts (schema reconciliation, metrics fetch).

- `Strict` — verify the chain against `rootCA` (or system trust store if
  unset) and check ServerName against the cert SANs. Handshake fails if the
  cert is invalid.
- `None` — equivalent to today's behavior: `InsecureSkipVerify=true`. Skip
  chain and hostname validation. Useful for local development against
  self-signed certs without ship-able CA bundles.
- Unset (`""`) — preserve legacy behavior. Same as `None` today.

The default is intentionally `None` (via "unset") so existing CHIs reconcile
unchanged on upgrade.

### `security.clickhouse.tls.minVersion`

Floors the TLS protocol version negotiated with ClickHouse hosts. Accepts
`"1.2"` or `"1.3"`. Empty uses Go's default (`1.2` today).

If the ClickHouse server doesn't support the requested floor, the handshake
fails with a clear `protocol version not supported` error.

### `security.clickhouse.tls.serverName`

Overrides the SNI / hostname used during TLS verification. By default the
operator uses the dial host (per-host FQDN derived from the CHI's cluster
shape). Set this when your certs are issued for a single reference name that
doesn't match per-pod FQDNs.

### `security.clickhouse.tls.rootCA`

PEM-encoded CA bundle (or base64-wrapped PEM — auto-detected). Used to verify
the ClickHouse host's cert when `verify: Strict`. If empty, the operator falls
back to the chopconf `access.rootCA`, then to the system trust store.

**Back-compat note**: setting `rootCA` alone — without `verify: Strict` — preserves
pre-0.27.1 behavior (`InsecureSkipVerify=true`). The bundle is loaded but not
enforced. To actually verify the chain against your CA, set `verify: Strict`
explicitly.

### `security.zookeeper.tls.verify` / `.minVersion`

Same semantics as the ClickHouse TLS knobs but applied to the operator's
ZooKeeper / Keeper client (used during initial cluster setup).

**These knobs apply ONLY when a TLS-enabled ZK dial is in flight** — i.e. when
the underlying `zookeeper.ConnectionParams` has `CertFile` / `KeyFile` set.
With a plain-TCP ZK endpoint (the default in many development environments),
the knobs are inert: there is no TLS handshake to configure. Setting
`verify: Strict` on a plain-TCP ZK does NOT upgrade the dial to TLS; it is
silently a no-op. To enforce TLS-protected ZK end-to-end, also configure
client cert/key/CA via the chopconf-level ZK section.

When TLS IS active, these knobs add explicit `MinVersion` and an
`InsecureSkipVerify` opt-out on top of the existing ZK TLS pipeline (which
always supplies `RootCAs` and `ServerName`).

### `security.kubernetes.tls.verify` (chopconf-only)

Operator-process-scoped — there is no CHI/cluster-level override. Gates startup
against the loaded kubeconfig's `TLSClientConfig.Insecure` field.

- `Strict` — refuse to start if the kubeconfig has `Insecure=true`. Typical
  for production operators that must never honor an accidentally-insecure
  kubeconfig.
- `None` — explicit opt-in to permit an insecure kubeconfig (development).
- Unset — preserve current behavior (kubeconfig wins).

Unlike `clickhouse.tls.verify` and `zookeeper.tls.verify`, this knob is a
LOAD-TIME GATE: the operator does not build the kubeconfig's `tls.Config`
(client-go does), so `Strict` only refuses startup — it does not actively
override the kubeconfig at the wire.

The check runs once at startup, after the chopconf is loaded — if the gate
fires, the operator exits with a `Fatal` log line including the exact problem.

### `security.kubernetes.tls.minVersion` (chopconf-only)

Declared for shape uniformity with ClickHouse/Zookeeper and coerced under FIPS,
but not yet enforced on the operator's K8s API transport. A future enhancement
will wire it into `rest.Config` when the operator wraps the kubeconfig with
stricter TLS settings.

### `security.ipc.mode`

Hardens the operator↔metrics-exporter REST channel. The exporter runs as a
sidecar in the operator's Pod and exposes `/chi` on port 8888 for the operator
to push CR/host registration. Without hardening, this endpoint binds all
interfaces and accepts unauthenticated requests from any pod on the same node
network.

- `Plain` (default) — preserve today's behavior. `/chi` binds all interfaces,
  no auth.
- `Secure` — the `/chi` handler enforces two checks:
  1. The remote address of the request must be loopback (`127.0.0.1`).
  2. An `X-CHOP-Token` header must match the per-Pod token at
     `/etc/clickhouse-operator-ipc/token`.

The token is generated by the operator at startup (32 bytes from
`crypto/rand`, hex-encoded → 64 chars) and written to a shared
`emptyDir{medium:Memory}` volume mounted into both containers. Token lifetime
= Pod lifetime; no rotation is required.

**Note**: In Secure mode the `/metrics` Prometheus endpoint still binds all
interfaces — only the `/chi` handler is loopback-restricted. ServiceMonitor /
Prometheus scrapes are unaffected.

**Container UID note**: The token file is written with mode `0o400` (owner-only
read). Operator and metrics-exporter containers MUST share a UID — or be in a
shared group via Pod-level `securityContext.fsGroup` — for the exporter to read
the token. The default Deployment satisfies this (both containers run as the
same user); custom per-container `securityContext` overrides that diverge UIDs
will break Secure mode at exporter startup.

### Externally-managed token (advanced)

The default flow generates a fresh per-Pod random token. If you need the token
to come from a Kubernetes Secret instead — for GitOps reproducibility, external
rotation by Vault / cert-manager / sealed-secrets, or audit/compliance reasons —
**no operator change is required**. Override the `clickhouse-operator-ipc`
volume in the operator Deployment from `emptyDir` to a `secret` projection
mounted at the same path:

```yaml
volumes:
  - name: clickhouse-operator-ipc
    secret:
      secretName: my-ipc-token
      items:
        - key: token
          path: token
          mode: 0400
```

The operator's startup logic at `pkg/chop/ipc_token.go` reuses any non-empty
file already present at `tokenPath`, so a pre-populated Secret-backed file is
adopted as-is and no random token is generated. Both containers continue to
read the same file via the shared mount — no client/server code path changes.

**Trade-offs vs the default `emptyDir{medium: Memory}` flow:**

- The token is now persisted in `etcd`. Verify your cluster has
  [encryption-at-rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/)
  enabled before relying on this; without it the token leaks into etcd backups.
- Rotation is your responsibility. Both containers cache the token in process
  memory after startup, so Secret edits do NOT propagate live — you must
  restart the operator Pod to pick up a rotated value.
- Entropy is your responsibility. The default flow guarantees 32 bytes from
  `crypto/rand`; a hand-rolled Secret could weaken this if it contains a short
  or predictable value. Recommend ≥32 random bytes hex-encoded.

This is intentionally a Deployment-level escape hatch, not a CRD field — the
IPC token is operator-internal trust material and users who don't need this
should keep the default `emptyDir` flow.

## Setup

The toggles below are pure CR fields. No new images, no new RBAC.

### Operator-wide via Helm

```yaml
# values.yaml
configs:
  files:
    config.yaml: |
      security:
        clickhouse:
          tls:
            verify: Strict
            minVersion: "1.3"
        ipc:
          mode: Secure
```

Then `helm upgrade clickhouse-operator altinity/clickhouse-operator -f values.yaml`.

### Operator-wide via ClickHouseOperatorConfiguration CR

```yaml
apiVersion: clickhouse.altinity.com/v1
kind: ClickHouseOperatorConfiguration
metadata:
  name: chop-config
spec:
  security:
    clickhouse:
      tls:
        verify: Strict
```

If `RestartOnOperatorConfigurationChange` is enabled (chopconf option), the
operator auto-restarts when this CR changes; otherwise restart the operator
pod manually for changes to apply.

### Per-CHI

```yaml
apiVersion: clickhouse.altinity.com/v1
kind: ClickHouseInstallation
metadata:
  name: my-chi
spec:
  configuration:
    clusters:
      - name: c1
        security:
          clickhouse:
            tls:
              verify: Strict
              rootCA: ...
```

Apply with `kubectl apply -f chi.yaml`. The operator re-normalizes on next
reconcile.

## Debug

### Verify a toggle is loaded

The operator logs the resolved chopconf at startup (level INFO):

```
$ kubectl logs -n kube-system deploy/clickhouse-operator -c clickhouse-operator | grep -i security
... Config parsed ...
security:
  clickhouse:
    tls:
      verify: "Strict"
      minVersion: "1.3"
  ipc:
    mode: "Secure"
```

### Check a CHI's resolved Security after inheritance

The 3-level merged values aren't directly exposed in CHI status. To inspect:

```bash
kubectl get chi <name> -o yaml | yq '.spec.configuration.clusters[].security'
```

That shows ONLY what's set at the cluster level. To see the effective merged
value, watch the operator logs during reconcile — TLS-setup paths emit:

```
TLS setup OK - root Cert registered (verify=Strict minVersion=1.3)
```

### TLS verify rejecting connections

If `verify: Strict` is set and connections start failing, check:

1. **Cert chain** — does your `rootCA` actually sign the ClickHouse server cert?
   ```bash
   openssl verify -CAfile rootca.pem clickhouse-server.crt
   ```
2. **SAN / hostname mismatch** — the cert's SANs must include the dial host
   the operator uses. Find the dial host in operator logs:
   ```
   Establishing connection: http://chi-<name>-<cluster>-<shard>-<replica>...
   ```
   Then inspect the cert:
   ```bash
   openssl s_client -connect <host>:8443 </dev/null 2>/dev/null \
     | openssl x509 -noout -text | grep -A1 'Subject Alternative Name'
   ```
   If the SANs don't match, either re-issue the cert with proper SANs (cleanest)
   or set `serverName:` to one of the existing SANs (workaround).
3. **MinVersion mismatch** — if the ClickHouse server is old and only supports
   1.2 but you set `minVersion: "1.3"`, handshakes will fail.

### IPC Secure mode debugging

If `ipc.mode: Secure` is enabled and the operator's CR registrations fail:

1. **Token presence on the exporter side**:
   ```bash
   kubectl exec -n kube-system deploy/clickhouse-operator -c metrics-exporter \
     -- sh -c '[ -r /etc/clickhouse-operator-ipc/token ] && echo readable'
   ```
   Should print `readable`. (The operator/exporter images are distroless and
   ship only `bash`/`sh`/`curl`; there is no `ls` or `stat` available.)

2. **Token presence on the operator side** (same path, same file — it's a
   shared volume):
   ```bash
   kubectl exec -n kube-system deploy/clickhouse-operator -c clickhouse-operator \
     -- sh -c '[ -r /etc/clickhouse-operator-ipc/token ] && echo readable'
   ```

3. **Reject reason in exporter logs**:
   ```bash
   kubectl logs -n kube-system deploy/clickhouse-operator -c metrics-exporter \
     | grep "IPC:"
   ```
   - `rejected non-loopback request from <addr>` — the operator is dialing
     non-loopback (shouldn't happen in normal operation — file a bug).
   - `rejected request from <addr> missing or invalid X-CHOP-Token header` —
     the operator's read of the token failed or the file content drifted.

4. **Operator side errors**:
   ```bash
   kubectl logs ... -c clickhouse-operator | grep "IPC Secure mode but token unreadable"
   ```

### Kubernetes tls.verify=Strict firing

The check runs once at startup. If you set it and the operator crash-loops
with the message:
```
kubeconfig declares TLSClientConfig.Insecure=true but
security.kubernetes.tls.verify=Strict — refusing to start
```
…then your kubeconfig (either the file mounted into the operator or the
in-cluster auto-discovered one) has `insecure-skip-tls-verify: true`. Either:
- Fix the kubeconfig (issue a CA-signed API-server cert and provide its CA in
  the kubeconfig), or
- Set `kubernetes.tls.verify: None` if you explicitly accept the dev posture,
  or leave the field unset to preserve pre-0.27.1 behavior.

## Upgrade compatibility

All toggles default to nil / unset such that an upgrade from 0.26.x
preserves identical runtime behavior:

- ClickHouse client still runs with `InsecureSkipVerify=true` until you opt in.
- ZooKeeper / Keeper TLS unchanged.
- Kubernetes client honors kubeconfig as before (unset `tls.verify` ≡ permissive).
- Operator↔exporter IPC is plain HTTP on all interfaces.
- Prometheus scrape topology unaffected (`/metrics` stays open even in Secure IPC mode; only `/chi` is loopback-restricted).

No CRD field is required, no Helm value is required. Existing chopconfs and
CHIs validate and apply unchanged.

**Upgrade ordering**: the new CRDs (with `security:` schema blocks) must be
applied BEFORE any CR using the `security:` block. `helm upgrade` handles this
automatically (CRDs ship in the chart). Manual installs must apply
`deploy/operator/clickhouse-operator-install-bundle.yaml` (which includes the
CRDs) first, then the CR. Applying a `security:`-bearing CR against a
pre-0.27.1 CRD returns `BadRequest: unknown field "spec.security"`.

**Typo handling**: the security schema blocks use
`x-kubernetes-preserve-unknown-fields: true`, so `kubectl apply` accepts unknown
field names without error. A typo like `tls.verifi: Strict` (missing 'y') is
silently swallowed and the operator falls through to default behavior. To
confirm a setting took effect, grep the operator logs for the relevant marker —
e.g. `TLS setup OK - root Cert registered (verify=Strict ...)` for TLS verify,
or `IPC: Secure mode — provisioned token` for IPC mode.

## Strict FIPS mode

The chopconf knob `security.fips.enforced: "yes"` is a master switch.
When enabled at startup, the operator:

1. **Coerces every per-component toggle to its Strict position** — logged at INFO
   per-field:
   - `security.clickhouse.tls.verify` → `Strict`
   - `security.clickhouse.tls.minVersion` → `1.3`
   - `security.zookeeper.tls.verify` → `Strict`
   - `security.zookeeper.tls.minVersion` → `1.3`
   - `security.kubernetes.tls.verify` → `Strict`
   - `security.kubernetes.tls.minVersion` → `1.3`
   - `security.ipc.mode` → `Secure`

   User-set values in any of these fields are overridden (one-way tightening).

2. **Rejects CHIs that reference plain-text external ZooKeeper.** Each
   `spec.configuration.zookeeper.nodes[].secure: true` is required; any node
   missing `secure: true` causes the CHI to land in `status: Aborted` with the
   bracketed reason `[FIPSValidationFailed]` in the error stream.

   The `secure: true` field is the enforced proxy for "FIPS-compatible
   ClickHouse Keeper over TLS" — plain-text ZK is not permitted under FIPS.

## FIPS image policy (`security.fips.images.policy`)

Orthogonal to `fips.enforced` — operators can run FIPS-strict TLS but accept
any image (for partial-FIPS pilots), or run legacy TLS while refusing
non-FIPS images (for image-audit rollouts), or combine both for a full FIPS
posture.

| `enforced` | `images.policy` | Result |
|---|---|---|
| `no` (default) | `Permissive` (default) | Legacy behavior — no FIPS gating. |
| `no` | `Required` | Reject CRs whose CH/Keeper images lack `fips` in the tag, or whose `SELECT version()` lacks `fips`. TLS knobs preserved. |
| `yes` | `Permissive` | Operator coerces TLS to Strict; images unchecked. |
| `yes` | `Required` | Full FIPS posture. |

### Detection signals

- **Admission (deploy-time)** — the operator's normalizer inspects each host's
  resolved PodTemplate `spec.containers[clickhouse].image` (or `keeper` for CHK)
  for the substring `fips` (case-insensitive) in the TAG portion of the
  reference. Registry-path substrings don't count. Hosts with no PodTemplate
  use the operator default `clickhouse/clickhouse-server:latest` (or the
  Keeper equivalent), which by construction fails Required.
- **Runtime (post-Ready)** — after the host responds to `SELECT version()`,
  the operator checks the reply for the same substring. Altinity FIPS builds
  bake the tag suffix (e.g. `.altinityfips`) into the binary's version
  string. Fails OPEN on transient SQL errors — a query hiccup against a
  running CR does NOT flip it to Aborted; the next reconcile re-evaluates.

### Failure reason

Reason tag `[FIPSImagePolicyViolation]` (distinct from
`[FIPSValidationFailed]`) is prepended to `status.errors`. Dashboards grep
either tag to distinguish operator-config bypass from per-CR image policy.

### Recovery from `[FIPSImagePolicyViolation]`

Edit the CHI/CHK to point at a FIPS-tagged image
(`altinity/clickhouse-server:<ver>.altinityfips`,
`altinity/clickhouse-keeper:<ver>.altinityfips`), then `kubectl apply`. The
informer's `UpdateFunc` re-enqueues; normalize re-runs cleanly.

Auto-recovery from pod-Ready transitions skips this reason (per
`shouldTriggerAutoRecovery`) — a pod flip can't fix a manifest that pins the
wrong image.

### Recovery from `[FIPSValidationFailed]`

The reason is encoded in `status.errors` (no first-class `reason` field; that
would be a CRD schema change). Operators and dashboards grep the error stream
for the bracketed tag:

```bash
kubectl get chi -o json | jq -r '.items[].status.errors[]? | select(startswith("[FIPSValidationFailed]"))'
```

Recovery is via spec edit: `kubectl apply` a corrected CHI (set `secure: true`
on every ZK node, or remove the `zookeeper:` block and use a CHK reference).
The informer's `UpdateFunc` re-enqueues the CR and normalize re-runs cleanly.
Note: this recovery path does NOT depend on `recovery.from.aborted.onPodReady`
— that path requires pod-readiness transitions, which never fire for CHIs
rejected at the normalizer (pods are never created).

### Out of scope for this knob

- **Forcing `/metrics` HTTPS** — ticket bullet deferred to a follow-up PR.
  Forcing HTTPS requires cert/key plumbing in the operator Deployment and a
  conditional ServiceMonitor scheme block in the Helm chart; both are non-
  trivial and break existing Prometheus scrape topology without warning.
- **Runtime FIPS detection via `crypto/fips140.Enforced()`** — requires the
  operator binary be built with the FIPS-validated Go toolchain
  (`GOFIPS140=v1.0.0`). When that build pipeline lands the runtime check will
  be OR'd with this config knob.
- **OperatorHub `features.operators.openshift.io/fips-compliant: "true"`
  label** — Red Hat policy requires a FIPS-validated binary; the label stays
  `"false"` until the FIPS build pipeline ships.
- **ClickHouseKeeperInstallation (CHK) controller** — the security toggles
  documented above apply to CHK as well via the shared ClusterSecurity type
  (spec-level + cluster-level), with the same chopconf inheritance and FIPS
  bypass-reject semantics. Symmetric Keeper-side TLS additions are tracked
  separately.

## Related

- See `docs/chi-examples/24-security-*.yaml` for concrete YAML examples.
- See `docs/chi-examples/70-chop-config.yaml` for the chopconf surface.
