# These requirements were auto generated
# from software requirements specification (SRS)
# document by TestFlows v2.0.231215.1221232.
# Do not edit by hand but re-generate instead
# using 'tfs requirements generate' command.
from testflows.core import Specification
from testflows.core import Requirement

Heading = Specification.Heading

RQ_SRS_026_ClickHouseOperator_FIPS_Config_ExternalTLS = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Config.ExternalTLS',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Plain HTTP/TCP on external connections SHALL be treated as a configuration error for FIPS compliance. TLS SHALL be enabled for connections to the [Kubernetes API], [ClickHouse Server], [ZooKeeper/Keeper], and Prometheus scrape endpoints.\n'
        '\n'
    ),
    link=None,
    level=2,
    num='2.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Build_ShippedBinaries = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Build.ShippedBinaries',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Each shipped pod binary — `clickhouse-operator` and `metrics-exporter` — SHALL satisfy all of the following:\n'
        '\n'
        '* Both binaries SHALL be built with `GOFIPS140=v1.0.0` (or `certified`); `go version -m` on each binary SHALL show the `GOFIPS140` build setting when the binary is inspectable.\n'
        '* Each binary SHALL identify itself as a FIPS build via `--version` output, `--fips-info`, or startup logs containing a FIPS indicator.\n'
        '* Each binary SHALL report `crypto/fips140.Version()` equal to `v1.0.0` (for example via `--fips-info` or in-process inspection).\n'
        '* Each binary SHALL report `crypto/fips140.Enabled()` equal to `true` when FIPS mode is active per `GODEBUG=fips140`.\n'
        '\n'
        'Examples:\n'
        '* `go version -m clickhouse-operator` contains `GOFIPS140=v1.0.0`\n'
        '* `go version -m metrics-exporter` contains `GOFIPS140=v1.0.0`\n'
        '* `clickhouse-operator --fips-info` reports:\n'
        '\n'
        '  ```yaml\n'
        '  fips_module:\n'
        '    version: v1.0.0\n'
        '    enabled: true\n'
        '  ```\n'
        '\n'
        '* `metrics-exporter --fips-info` reports:\n'
        '\n'
        '  ```yaml\n'
        '  fips_module:\n'
        '    version: v1.0.0\n'
        '    enabled: true\n'
        '  ```\n'
        '\n'
    ),
    link=None,
    level=3,
    num='3.1.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Build_ShippedBinaries_StartupLogs = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Build.ShippedBinaries.StartupLogs',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'At startup, each binary SHALL emit a FIPS startup banner in logs indicating build and runtime FIPS state.\n'
        '\n'
        'when GODEBUG=fips140=only:\n'
        '\n'
        '```text\n'
        'FIPS: chopconf.fips.enforced=true \\\n'
        'build.linked=true \\\n'
        'module.active=true \\\n'
        'runtime.enforced=true \\\n'
        'module=v1.0.0\n'
        '```\n'
        '\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='3.1.2'
)

RQ_SRS_026_ClickHouseOperator_FIPS_TLS_ApprovedCiphers = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.TLS.ApprovedCiphers',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'TLS-enforced external connections for [clickhouse-operator] and [metrics-exporter]\n'
        'SHALL negotiate only TLS 1.3 with the following approved cipher suites.\n'
        '\n'
        '| Cipher Suite | OpenSSL Name |\n'
        '|--------------|--------------|\n'
        '| TLS_AES_128_GCM_SHA256 | TLS_AES_128_GCM_SHA256 |\n'
        '| TLS_AES_256_GCM_SHA384 | TLS_AES_256_GCM_SHA384 |\n'
        '| TLS_AES_128_CCM_SHA256 | TLS_AES_128_CCM_SHA256 |\n'
        '| TLS_AES_128_CCM_8_SHA256 | TLS_AES_128_CCM_8_SHA256 |\n'
        '\n'
    ),
    link=None,
    level=2,
    num='4.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_TLS_RejectedCiphers = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.TLS.RejectedCiphers',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'TLS connections SHALL reject the following for all TLS-enabled external connections:\n'
        '\n'
        '- Any TLS cipher suite not explicitly listed in [RQ.SRS-026.ClickHouseOperator.FIPS.TLS.ApprovedCiphers](#rqsrs-026clickhouseoperatorfipstlsapprovedciphers)\n'
        '- Protocol versions: SSLv2, SSLv3, TLS 1.0, TLS 1.1\n'
        '- Cipher suites using non-approved/legacy algorithms (for this profile), including:\n'
        '  - ChaCha20-Poly1305\n'
        '  - RC4, RC2, DES, 3DES, IDEA, SEED, CAMELLIA, ARIA\n'
        '  - NULL encryption / NULL authentication\n'
        '  - Anonymous key exchange (`aNULL`, `eNULL`, `ADH`, `AECDH`)\n'
        '  - Export/weak suites (`EXP`, `LOW`, `40-bit`, `56-bit`)\n'
        '  - MD5- or SHA-1-based legacy suites\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='4.2.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_FIPSConfig = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.FIPSConfig',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Deploying a CHI with FIPS TLS settings SHALL start ClickHouse with FIPS-compliant TLS configuration.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.1.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHIDeploy = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHIDeploy',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The operator SHALL deploy FIPS `ClickHouseInstallation` resources to `Completed` with Running pods when configuration is valid.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.1.2'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_NoPlainHTTP = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.NoPlainHTTP',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'When FIPS transport hardening applies, ClickHouse pods SHALL NOT listen on plain HTTP port 8123; HTTPS port 8443 SHALL be used.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.1.3'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_NoPlainNative = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.NoPlainNative',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'When FIPS transport hardening applies, ClickHouse pods SHALL NOT listen on plain native TCP port 9000; secure native port 9440 SHALL be used.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.1.4'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_NoUnexpectedPorts = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.NoUnexpectedPorts',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'ClickHouse pods in a FIPS deployment SHALL expose only expected secure listener ports and no additional unexpected ports.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.1.5'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_InternodeTLS = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.InternodeTLS',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'ReplicatedMergeTree replicas SHALL communicate over interserver HTTPS (`interserver_https_port`) and data SHALL converge across replicas.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.1.6'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_ScaleUp = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.ScaleUp',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Adding a replica to a FIPS-configured CHI SHALL reconcile to `Completed` and the new replica SHALL run the FIPS ClickHouse binary with TLS-only listeners.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.1.7'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_ScaleDown = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.ScaleDown',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Removing a replica from a FIPS-configured CHI SHALL reconcile to `Completed` and remaining replicas SHALL keep FIPS binary and TLS-only configuration.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.1.8'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_ConfigUpdate = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.ConfigUpdate',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Updating TLS settings on a running CHI SHALL reload ClickHouse with the new FIPS-compliant configuration.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.1.9'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_FIPSConfig = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.FIPSConfig',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Deploying a CHK with FIPS TLS settings SHALL start Keeper with FIPS-compliant TLS configuration.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.2.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHKDeploy = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHKDeploy',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The operator SHALL deploy FIPS `ClickHouseKeeperInstallation` resources to `Completed` with Running pods when configuration is valid.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.2.2'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_NoPlainClientPort = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.NoPlainClientPort',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'When FIPS transport hardening applies, Keeper pods SHALL NOT listen on plain client port 2181; secure client port 2281 SHALL be used.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.2.3'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_NoUnexpectedPorts = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.NoUnexpectedPorts',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Keeper pods in a FIPS deployment SHALL expose only expected secure listener ports.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.2.4'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_RaftTLS = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.RaftTLS',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Keeper Raft communication SHALL use TLS on the configured secure Raft port.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.2.5'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_ScaleUp = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.ScaleUp',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Adding a node to a FIPS-configured Keeper cluster SHALL reconcile to `Completed` and the new node SHALL run the FIPS Keeper binary with TLS-only client and Raft listeners.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.2.6'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_ScaleDown = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.ScaleDown',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Removing a node from a FIPS-configured Keeper cluster SHALL reconcile to `Completed` and remaining nodes SHALL keep FIPS configuration.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.2.7'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_ConfigUpdate = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.ConfigUpdate',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Updating TLS settings on a running CHK SHALL reload Keeper with the new FIPS-compliant configuration.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.2.8'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_VersionString = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.VersionString',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'A running ClickHouse host under FIPS image policy SHALL report a `version()` string containing `fips` (case-insensitive).\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.3.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_FIPSBinary = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.FIPSBinary',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The `clickhouse-backup` sidecar SHALL run a FIPS-built binary; `clickhouse-backup --version` SHALL contain `fips` (case-insensitive).\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.3.2'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_GOFIPS140 = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.GOFIPS140',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'When inspectable, the clickhouse-backup sidecar binary SHALL embed `GOFIPS140=v1.0.0` per `go version -m`.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.3.3'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_OnlyTLSPorts = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.OnlyTLSPorts',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The clickhouse-backup sidecar SHALL expose only secure listener ports (including HTTPS API port 7171).\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.3.4'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_HTTPSAPI = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.HTTPSAPI',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The clickhouse-backup HTTPS API SHALL serve over TLS with CA-trust enforcement: trusted clients accepted, untrusted clients rejected.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.3.5'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_ClickHouseOverTLS = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.ClickHouseOverTLS',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The clickhouse-backup sidecar SHALL reach ClickHouse over secure native TCP.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.3.6'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_RestoreRoundTrip = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.RestoreRoundTrip',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Backup and restore through the HTTPS API SHALL succeed over TLS.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.3.7'
)

RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_RemoteUploadTLS = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.RemoteUploadTLS',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Remote backup upload to object storage SHALL use FIPS-approved TLS.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='5.3.8'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_CoerceVerifyStrict = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.CoerceVerifyStrict',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'With `fips.enforced=true`, unset TLS verify SHALL be coerced to Strict for ClickHouse, ZooKeeper/Keeper, and Kubernetes clients.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.1.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_CoerceMinVersion13 = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.CoerceMinVersion13',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'With `fips.enforced=true`, unset TLS minVersion SHALL be coerced to 1.3 for the\n'
        "operator's outbound TLS clients.\n"
        '\n'
    ),
    link=None,
    level=3,
    num='6.1.2'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_OverrideMinVersion12To13 = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.OverrideMinVersion12To13',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'When `security.fips.enforced: "true"` is set in the [ClickHouseOperatorConfiguration], the operator SHALL coerce `minVersion` to `"1.3"` for `security.clickhouse.tls`, `security.zookeeper.tls`, and `security.kubernetes.tls`, even when those fields are explicitly set to `"1.2"`.\n'
        '\n'
        '```yaml\n'
        'spec:\n'
        '  security:\n'
        '    fips:\n'
        '      enforced: "true"\n'
        '    clickhouse:\n'
        '      tls:\n'
        '        minVersion: "1.2"\n'
        '    zookeeper:\n'
        '      tls:\n'
        '        minVersion: "1.2"\n'
        '    kubernetes:\n'
        '      tls:\n'
        '        minVersion: "1.2"\n'
        '```\n'
        '\n'
        'After operator configuration normalization, the effective `minVersion` for each component listed above SHALL be `"1.3"`.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.1.3'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_CoerceIPCSecure = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.CoerceIPCSecure',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'With `fips.enforced=true`, unset IPC mode SHALL be coerced to Secure.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.1.4'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_RejectInsecureKubeconfig = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectInsecureKubeconfig',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The operator SHALL refuse to start when kubeconfig uses `TLSClientConfig.Insecure=true` under strict/FIPS mode.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.1.5'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_RejectVerifyNoneCHI = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectVerifyNoneCHI',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'CHI with `clickhouse.tls.verify=None` under enforced mode SHALL be rejected with `FIPSValidationFailed`.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.1.6'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_RejectVerifyNoneZK = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectVerifyNoneZK',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'CHI with `zookeeper.tls.verify=None` under enforced mode SHALL be rejected.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.1.7'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_RejectInvalidMinVersion = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectInvalidMinVersion',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'CHI with invalid TLS minVersion under enforced mode SHALL be rejected.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.1.8'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_RejectExternalZookeeper = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectExternalZookeeper',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'CHI referencing plain external ZooKeeper nodes under enforced mode SHALL be rejected.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.1.9'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_RejectCHKBypass = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectCHKBypass',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'CHK with TLS verify bypass under enforced mode SHALL be rejected.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.1.10'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_MinVersionScope = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.MinVersionScope',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The `minVersion` coercion SHALL apply only to TLS clients created and managed by the operator.\n'
        'They SHALL NOT require ClickHouse Server or ClickHouse Keeper listener endpoints to reject TLS 1.2.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.1.11'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Images_Required_RejectCHI = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.RejectCHI',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'With `security.fips.images.policy=Required`, CHI with non-FIPS image tag SHALL be rejected with `FIPSImagePolicyViolation`.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.2.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Images_Required_AcceptCHI = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.AcceptCHI',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'With image policy Required, CHI with FIPS-tagged image SHALL reconcile normally.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.2.2'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Images_Required_RejectCHK = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.RejectCHK',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'With image policy Required, CHK with non-FIPS Keeper image SHALL be rejected.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.2.3'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Images_Required_RuntimeVersion = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.RuntimeVersion',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'With image policy Required, host `SELECT version()` lacking `fips` SHALL fail with `FIPSImagePolicyViolation`.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.2.4'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Images_Permissive = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.Permissive',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'With permissive image policy, non-FIPS CHI images SHALL reconcile (default).\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.2.5'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Images_Required_ShortCircuit = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.ShortCircuit',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Multiple non-FIPS hosts SHALL produce a single policy violation error.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.2.6'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Images_TagDetection_FIPSSuffix = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.FIPSSuffix',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Image tags containing `fips` (case-insensitive) SHALL be detected as FIPS.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.3.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Images_TagDetection_AltinityFIPS = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.AltinityFIPS',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Image tags containing `altinityfips` SHALL be detected as FIPS.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.3.2'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Images_TagDetection_DigestOnly = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.DigestOnly',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Digest-only image references SHALL NOT be detected as FIPS at admission.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.3.3'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Images_TagDetection_RegistryPath = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.RegistryPath',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Registry hostname containing `fips` SHALL NOT satisfy FIPS tag detection.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.3.4'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Images_TagDetection_CaseInsensitive = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.CaseInsensitive',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Image tags such as `25.3.FIPS` or `25.3.Fips` SHALL be detected as FIPS (case-insensitive match on the tag).\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='6.3.5'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Operator_Listeners = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.Listeners',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'FIPS workload pods (ClickHouse, Keeper, and sidecar containers) SHALL listen only on expected TLS ports. Plaintext service ports (8123, 9000, 2181) SHALL NOT be open when FIPS transport hardening applies.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='7.1.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Operator_Kubernetes = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.Kubernetes',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The operator SHALL connect to the Kubernetes API using FIPS-approved TLS ciphers.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='7.2.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Operator_ClickHouse = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.ClickHouse',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The operator SHALL connect to ClickHouse using FIPS-approved TLS ciphers.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='7.3.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Operator_Zookeeper = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.Zookeeper',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The operator SHALL connect to ZooKeeper/Keeper using FIPS-approved TLS ciphers.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='7.4.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Operator_IPCSecure = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.IPCSecure',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Operator IPC with `security.ipc.mode=Secure` SHALL work over localhost HTTP with token auth.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='7.5.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Gap_OperatorMetricsTLS = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Gap.OperatorMetricsTLS',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Operator Prometheus metrics on :9999 currently expose a known FIPS gap (HTTP-only).\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='7.6.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Exporter_Listeners = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Exporter.Listeners',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The metrics-exporter process SHALL expose only expected listener ports on `:8888`. Sidecar containers in the same pod SHALL be listener-audited with the same `/proc/net/tcp` procedure.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='8.1.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Exporter_Kubernetes = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Exporter.Kubernetes',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The exporter SHALL connect to the Kubernetes API using FIPS-approved TLS ciphers.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='8.2.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Exporter_ClickHouse = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Exporter.ClickHouse',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The exporter SHALL query ClickHouse using FIPS-approved TLS when configured for HTTPS.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='8.3.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Gap_ExporterMetricsTLS = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Gap.ExporterMetricsTLS',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Exporter Prometheus metrics on :8888 currently expose a known FIPS gap (HTTP-only).\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='8.4.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Integrity_OperatorMismatch = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Integrity.OperatorMismatch',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Tampering with `clickhouse-operator` `.go.fipsinfo` SHALL panic with `fips140: verification mismatch`.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='9.1.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Integrity_ExporterMismatch = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Integrity.ExporterMismatch',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Tampering with `metrics-exporter` `.go.fipsinfo` SHALL panic with `fips140: verification mismatch`.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='9.2.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_CAST_OperatorFail = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.CAST.OperatorFail',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Running `clickhouse-operator` with `GODEBUG=failfipscast=<name>` SHALL terminate with a CAST error.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='10.1.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_CAST_ExporterFail = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.CAST.ExporterFail',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Running `metrics-exporter` with `GODEBUG=failfipscast=<name>` SHALL terminate with a CAST error.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='10.2.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Synthetic_ApprovedCiphers = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Synthetic.ApprovedCiphers',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'For each external connection listed below, when exercised as a TLS **client** with `openssl s_server` offering only [approved ciphers](#rqsrs-026clickhouseoperatorfipstlsapprovedciphers), or as a TLS **server** with `openssl s_client` using only approved ciphers, the connection SHALL succeed:\n'
        '\n'
        '| Connection | Role | Tool |\n'
        '|------------|------|------|\n'
        '| Operator to Kubernetes API | Client | `openssl s_server` |\n'
        '| Operator to ClickHouse Server | Client | `openssl s_server` |\n'
        '| Operator to ZooKeeper/Keeper | Client | `openssl s_server` |\n'
        '| Operator metrics :9999 | Server | `openssl s_client` |\n'
        '| Exporter to Kubernetes API | Client | `openssl s_server` |\n'
        '| Exporter to ClickHouse Server | Client | `openssl s_server` |\n'
        '| Exporter metrics :8888 | Server | `openssl s_client` |\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='11.1.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_Synthetic_RejectedCiphers = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.Synthetic.RejectedCiphers',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'For each external connection listed below, when the peer offers only [rejected ciphers or protocols](#rqsrs-026clickhouseoperatorfipstlsrejectedciphers), the connection SHALL be rejected:\n'
        '\n'
        '| Connection | Role | Tool |\n'
        '|------------|------|------|\n'
        '| Operator to Kubernetes API | Client | `openssl s_server` |\n'
        '| Operator to ClickHouse Server | Client | `openssl s_server` |\n'
        '| Operator to ZooKeeper/Keeper | Client | `openssl s_server` |\n'
        '| Operator metrics :9999 | Server | `openssl s_client` |\n'
        '| Exporter to Kubernetes API | Client | `openssl s_server` |\n'
        '| Exporter to ClickHouse Server | Client | `openssl s_server` |\n'
        '| Exporter metrics :8888 | Server | `openssl s_client` |\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='11.2.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_CICD_OperatorImageBuild = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.CICD.OperatorImageBuild',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'CI SHALL build the [clickhouse-operator] FIPS image successfully.\n'
        '\n'
    ),
    link=None,
    level=2,
    num='12.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_CICD_ExporterImageBuild = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.CICD.ExporterImageBuild',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'CI SHALL build the [metrics-exporter] FIPS image successfully.\n'
        '\n'
    ),
    link=None,
    level=2,
    num='12.2'
)

RQ_SRS_026_ClickHouseOperator_FIPS_CICD_VulnerabilityScan = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.CICD.VulnerabilityScan',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'FIPS images SHALL pass vulnerability scanning with no Critical, High, or Medium findings.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=2,
    num='12.3'
)

RQ_SRS_026_ClickHouseOperator_FIPS_AIReview_Operator_Tree = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Operator.Tree',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Static review of operator-scoped paths SHALL produce no Critical findings; Warning-level findings SHALL be documented.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='12.4.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_AIReview_Operator_SharedPkg = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Operator.SharedPkg',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Review of shared packages reachable from `cmd/operator` SHALL produce no Critical findings.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='12.4.2'
)

RQ_SRS_026_ClickHouseOperator_FIPS_AIReview_Operator_RegressionGate = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Operator.RegressionGate',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'A signed-off review artifact SHALL be stored with the build record before release.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='12.4.3'
)

RQ_SRS_026_ClickHouseOperator_FIPS_AIReview_Exporter_Tree = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Exporter.Tree',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Static review of exporter-scoped paths SHALL produce no Critical findings; Warning-level findings SHALL be documented.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='12.5.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_AIReview_Exporter_SharedPkg = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Exporter.SharedPkg',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Review of shared packages reachable from `cmd/metrics_exporter` SHALL produce no Critical findings.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='12.5.2'
)

RQ_SRS_026_ClickHouseOperator_FIPS_AIReview_Exporter_RegressionGate = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Exporter.RegressionGate',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'A signed-off review artifact SHALL be stored with the build record before release.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='12.5.3'
)

RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Operator_WrapperIntegration = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.WrapperIntegration',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Building clickhouse-operator with `-tags acvp_wrapper` SHALL expose a working ACVP responder via argv0 dispatch.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='13.1.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Operator_ConfigGeneration = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.ConfigGeneration',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The clickhouse-operator ACVP responder SHALL answer `getConfig` with supported capabilities.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='13.1.2'
)

RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Operator_ExpectedOutputReplay = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.ExpectedOutputReplay',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        '`bash pkg/util/fips/acvp/run.sh` SHALL match all configured expected outputs for the operator.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='13.1.3'
)

RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Operator_SuiteCount = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.SuiteCount',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The tracked ACVP config SHALL report 38 matched expectations for clickhouse-operator.\n'
        '\n'
        '\n'
    ),
    link=None,
    level=3,
    num='13.1.4'
)

RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Exporter_WrapperIntegration = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.WrapperIntegration',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'Building metrics-exporter with `-tags acvp_wrapper` SHALL expose a working ACVP responder.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='13.2.1'
)

RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Exporter_ConfigGeneration = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.ConfigGeneration',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The metrics-exporter ACVP responder SHALL answer `getConfig` with supported capabilities.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='13.2.2'
)

RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Exporter_ExpectedOutputReplay = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.ExpectedOutputReplay',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        '`BINARY=metrics-exporter bash pkg/util/fips/acvp/run.sh` SHALL match all expected outputs.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='13.2.3'
)

RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Exporter_SuiteCount = Requirement(
    name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.SuiteCount',
    version='1.0',
    priority=None,
    group=None,
    type=None,
    uid=None,
    description=(
        'The tracked ACVP config SHALL report 38 matched expectations for metrics-exporter.\n'
        '\n'
    ),
    link=None,
    level=3,
    num='13.2.4'
)

Inbound_connection_to_operator_exporter_metrics_endpoint = Specification(
    name='Inbound connection to operator/exporter metrics endpoint',
    description=None,
    author=None,
    date=None,
    status=None,
    approved_by=None,
    approved_date=None,
    approved_version=None,
    version=None,
    group=None,
    type=None,
    link=None,
    uid=None,
    parent=None,
    children=None,
    headings=(
        Heading(name='Introduction', level=1, num='1'),
        Heading(name='Configuration Requirements', level=1, num='2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Config.ExternalTLS', level=2, num='2.1'),
        Heading(name='Build Verification', level=1, num='3'),
        Heading(name='Shipped Binaries', level=2, num='3.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Build.ShippedBinaries', level=3, num='3.1.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Build.ShippedBinaries.StartupLogs', level=3, num='3.1.2'),
        Heading(name='Approved TLS Cipher Suites', level=1, num='4'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.TLS.ApprovedCiphers', level=2, num='4.1'),
        Heading(name='Rejected Cipher Suites and Protocols', level=2, num='4.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.TLS.RejectedCiphers', level=3, num='4.2.1'),
        Heading(name='ClickHouse Server and Keeper FIPS Configurations', level=1, num='5'),
        Heading(name='ClickHouse Server', level=2, num='5.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.FIPSConfig', level=3, num='5.1.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHIDeploy', level=3, num='5.1.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.NoPlainHTTP', level=3, num='5.1.3'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.NoPlainNative', level=3, num='5.1.4'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.NoUnexpectedPorts', level=3, num='5.1.5'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.InternodeTLS', level=3, num='5.1.6'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.ScaleUp', level=3, num='5.1.7'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.ScaleDown', level=3, num='5.1.8'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.ConfigUpdate', level=3, num='5.1.9'),
        Heading(name='ClickHouse Keeper', level=2, num='5.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.FIPSConfig', level=3, num='5.2.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHKDeploy', level=3, num='5.2.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.NoPlainClientPort', level=3, num='5.2.3'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.NoUnexpectedPorts', level=3, num='5.2.4'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.RaftTLS', level=3, num='5.2.5'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.ScaleUp', level=3, num='5.2.6'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.ScaleDown', level=3, num='5.2.7'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.ConfigUpdate', level=3, num='5.2.8'),
        Heading(name='ClickHouse Backup Sidecar', level=2, num='5.3'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.VersionString', level=3, num='5.3.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.FIPSBinary', level=3, num='5.3.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.GOFIPS140', level=3, num='5.3.3'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.OnlyTLSPorts', level=3, num='5.3.4'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.HTTPSAPI', level=3, num='5.3.5'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.ClickHouseOverTLS', level=3, num='5.3.6'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.RestoreRoundTrip', level=3, num='5.3.7'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.RemoteUploadTLS', level=3, num='5.3.8'),
        Heading(name='FIPS Enforcement Mode', level=1, num='6'),
        Heading(name='Security Coercion', level=2, num='6.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.CoerceVerifyStrict', level=3, num='6.1.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.CoerceMinVersion13', level=3, num='6.1.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.OverrideMinVersion12To13', level=3, num='6.1.3'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.CoerceIPCSecure', level=3, num='6.1.4'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectInsecureKubeconfig', level=3, num='6.1.5'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectVerifyNoneCHI', level=3, num='6.1.6'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectVerifyNoneZK', level=3, num='6.1.7'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectInvalidMinVersion', level=3, num='6.1.8'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectExternalZookeeper', level=3, num='6.1.9'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectCHKBypass', level=3, num='6.1.10'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.MinVersionScope', level=3, num='6.1.11'),
        Heading(name='Image Policy', level=2, num='6.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.RejectCHI', level=3, num='6.2.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.AcceptCHI', level=3, num='6.2.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.RejectCHK', level=3, num='6.2.3'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.RuntimeVersion', level=3, num='6.2.4'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.Permissive', level=3, num='6.2.5'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.ShortCircuit', level=3, num='6.2.6'),
        Heading(name='Image Tag Detection', level=2, num='6.3'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.FIPSSuffix', level=3, num='6.3.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.AltinityFIPS', level=3, num='6.3.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.DigestOnly', level=3, num='6.3.3'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.RegistryPath', level=3, num='6.3.4'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.CaseInsensitive', level=3, num='6.3.5'),
        Heading(name='Operator External Connections', level=1, num='7'),
        Heading(name='Operator Runtime Listener Verification', level=2, num='7.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.Listeners', level=3, num='7.1.1'),
        Heading(name='Operator to Kubernetes API', level=2, num='7.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.Kubernetes', level=3, num='7.2.1'),
        Heading(name='Operator to ClickHouse Server', level=2, num='7.3'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.ClickHouse', level=3, num='7.3.1'),
        Heading(name='Operator to ZooKeeper/Keeper', level=2, num='7.4'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.Zookeeper', level=3, num='7.4.1'),
        Heading(name='Operator to metrics-exporter IPC', level=2, num='7.5'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.IPCSecure', level=3, num='7.5.1'),
        Heading(name='Operator Prometheus Metrics', level=2, num='7.6'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Gap.OperatorMetricsTLS', level=3, num='7.6.1'),
        Heading(name='Exporter External Connections', level=1, num='8'),
        Heading(name='Exporter Runtime Listener Verification', level=2, num='8.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Exporter.Listeners', level=3, num='8.1.1'),
        Heading(name='Exporter to Kubernetes API', level=2, num='8.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Exporter.Kubernetes', level=3, num='8.2.1'),
        Heading(name='Exporter to ClickHouse Server', level=2, num='8.3'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Exporter.ClickHouse', level=3, num='8.3.1'),
        Heading(name='Exporter Prometheus Metrics', level=2, num='8.4'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Gap.ExporterMetricsTLS', level=3, num='8.4.1'),
        Heading(name='Integrity Check Failure', level=1, num='9'),
        Heading(name='Operator Integrity Tampering', level=2, num='9.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Integrity.OperatorMismatch', level=3, num='9.1.1'),
        Heading(name='Exporter Integrity Tampering', level=2, num='9.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Integrity.ExporterMismatch', level=3, num='9.2.1'),
        Heading(name='CAST Failure', level=1, num='10'),
        Heading(name='Operator CAST Failure', level=2, num='10.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.CAST.OperatorFail', level=3, num='10.1.1'),
        Heading(name='Exporter CAST Failure', level=2, num='10.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.CAST.ExporterFail', level=3, num='10.2.1'),
        Heading(name='Synthetic TLS Cipher Validation', level=1, num='11'),
        Heading(name='Operator as TLS client against server offering non-approved cipher', level=0, num=''),
        Heading(name='Approved cipher matrix', level=2, num='11.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Synthetic.ApprovedCiphers', level=3, num='11.1.1'),
        Heading(name='Rejected cipher matrix', level=2, num='11.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.Synthetic.RejectedCiphers', level=3, num='11.2.1'),
        Heading(name='CI/CD Image and Policy Verification', level=1, num='12'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.CICD.OperatorImageBuild', level=2, num='12.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.CICD.ExporterImageBuild', level=2, num='12.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.CICD.VulnerabilityScan', level=2, num='12.3'),
        Heading(name='Operator Source Review', level=2, num='12.4'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Operator.Tree', level=3, num='12.4.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Operator.SharedPkg', level=3, num='12.4.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Operator.RegressionGate', level=3, num='12.4.3'),
        Heading(name='Exporter Source Review', level=2, num='12.5'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Exporter.Tree', level=3, num='12.5.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Exporter.SharedPkg', level=3, num='12.5.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Exporter.RegressionGate', level=3, num='12.5.3'),
        Heading(name='ACVP Algorithm Validation', level=1, num='13'),
        Heading(name='Operator ACVP Validation', level=2, num='13.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.WrapperIntegration', level=3, num='13.1.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.ConfigGeneration', level=3, num='13.1.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.ExpectedOutputReplay', level=3, num='13.1.3'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.SuiteCount', level=3, num='13.1.4'),
        Heading(name='Exporter ACVP Validation', level=2, num='13.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.WrapperIntegration', level=3, num='13.2.1'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.ConfigGeneration', level=3, num='13.2.2'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.ExpectedOutputReplay', level=3, num='13.2.3'),
        Heading(name='RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.SuiteCount', level=3, num='13.2.4'),
        Heading(name='Terminology', level=1, num='14'),
        Heading(name='SRS', level=2, num='14.1'),
        Heading(name='FIPS 140-3', level=2, num='14.2'),
        Heading(name='clickhouse-operator', level=2, num='14.3'),
        Heading(name='metrics-exporter', level=2, num='14.4'),
        Heading(name='CHI', level=2, num='14.5'),
        Heading(name='CHK', level=2, num='14.6'),
        Heading(name='ACVP', level=2, num='14.7'),
        Heading(name='CMVP', level=2, num='14.8'),
        Heading(name='CAVP', level=2, num='14.9'),
        ),
    requirements=(
        RQ_SRS_026_ClickHouseOperator_FIPS_Config_ExternalTLS,
        RQ_SRS_026_ClickHouseOperator_FIPS_Build_ShippedBinaries,
        RQ_SRS_026_ClickHouseOperator_FIPS_Build_ShippedBinaries_StartupLogs,
        RQ_SRS_026_ClickHouseOperator_FIPS_TLS_ApprovedCiphers,
        RQ_SRS_026_ClickHouseOperator_FIPS_TLS_RejectedCiphers,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_FIPSConfig,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHIDeploy,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_NoPlainHTTP,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_NoPlainNative,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_NoUnexpectedPorts,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_InternodeTLS,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_ScaleUp,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_ScaleDown,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_ConfigUpdate,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_FIPSConfig,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHKDeploy,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_NoPlainClientPort,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_NoUnexpectedPorts,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_RaftTLS,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_ScaleUp,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_ScaleDown,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CHK_ConfigUpdate,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_CH_VersionString,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_FIPSBinary,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_GOFIPS140,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_OnlyTLSPorts,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_HTTPSAPI,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_ClickHouseOverTLS,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_RestoreRoundTrip,
        RQ_SRS_026_ClickHouseOperator_FIPS_DataPlane_Backup_RemoteUploadTLS,
        RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_CoerceVerifyStrict,
        RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_CoerceMinVersion13,
        RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_OverrideMinVersion12To13,
        RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_CoerceIPCSecure,
        RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_RejectInsecureKubeconfig,
        RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_RejectVerifyNoneCHI,
        RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_RejectVerifyNoneZK,
        RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_RejectInvalidMinVersion,
        RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_RejectExternalZookeeper,
        RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_RejectCHKBypass,
        RQ_SRS_026_ClickHouseOperator_FIPS_Enforced_MinVersionScope,
        RQ_SRS_026_ClickHouseOperator_FIPS_Images_Required_RejectCHI,
        RQ_SRS_026_ClickHouseOperator_FIPS_Images_Required_AcceptCHI,
        RQ_SRS_026_ClickHouseOperator_FIPS_Images_Required_RejectCHK,
        RQ_SRS_026_ClickHouseOperator_FIPS_Images_Required_RuntimeVersion,
        RQ_SRS_026_ClickHouseOperator_FIPS_Images_Permissive,
        RQ_SRS_026_ClickHouseOperator_FIPS_Images_Required_ShortCircuit,
        RQ_SRS_026_ClickHouseOperator_FIPS_Images_TagDetection_FIPSSuffix,
        RQ_SRS_026_ClickHouseOperator_FIPS_Images_TagDetection_AltinityFIPS,
        RQ_SRS_026_ClickHouseOperator_FIPS_Images_TagDetection_DigestOnly,
        RQ_SRS_026_ClickHouseOperator_FIPS_Images_TagDetection_RegistryPath,
        RQ_SRS_026_ClickHouseOperator_FIPS_Images_TagDetection_CaseInsensitive,
        RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Operator_Listeners,
        RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Operator_Kubernetes,
        RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Operator_ClickHouse,
        RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Operator_Zookeeper,
        RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Operator_IPCSecure,
        RQ_SRS_026_ClickHouseOperator_FIPS_Gap_OperatorMetricsTLS,
        RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Exporter_Listeners,
        RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Exporter_Kubernetes,
        RQ_SRS_026_ClickHouseOperator_FIPS_Connect_Exporter_ClickHouse,
        RQ_SRS_026_ClickHouseOperator_FIPS_Gap_ExporterMetricsTLS,
        RQ_SRS_026_ClickHouseOperator_FIPS_Integrity_OperatorMismatch,
        RQ_SRS_026_ClickHouseOperator_FIPS_Integrity_ExporterMismatch,
        RQ_SRS_026_ClickHouseOperator_FIPS_CAST_OperatorFail,
        RQ_SRS_026_ClickHouseOperator_FIPS_CAST_ExporterFail,
        RQ_SRS_026_ClickHouseOperator_FIPS_Synthetic_ApprovedCiphers,
        RQ_SRS_026_ClickHouseOperator_FIPS_Synthetic_RejectedCiphers,
        RQ_SRS_026_ClickHouseOperator_FIPS_CICD_OperatorImageBuild,
        RQ_SRS_026_ClickHouseOperator_FIPS_CICD_ExporterImageBuild,
        RQ_SRS_026_ClickHouseOperator_FIPS_CICD_VulnerabilityScan,
        RQ_SRS_026_ClickHouseOperator_FIPS_AIReview_Operator_Tree,
        RQ_SRS_026_ClickHouseOperator_FIPS_AIReview_Operator_SharedPkg,
        RQ_SRS_026_ClickHouseOperator_FIPS_AIReview_Operator_RegressionGate,
        RQ_SRS_026_ClickHouseOperator_FIPS_AIReview_Exporter_Tree,
        RQ_SRS_026_ClickHouseOperator_FIPS_AIReview_Exporter_SharedPkg,
        RQ_SRS_026_ClickHouseOperator_FIPS_AIReview_Exporter_RegressionGate,
        RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Operator_WrapperIntegration,
        RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Operator_ConfigGeneration,
        RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Operator_ExpectedOutputReplay,
        RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Operator_SuiteCount,
        RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Exporter_WrapperIntegration,
        RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Exporter_ConfigGeneration,
        RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Exporter_ExpectedOutputReplay,
        RQ_SRS_026_ClickHouseOperator_FIPS_ACVP_Exporter_SuiteCount,
        ),
    content='''
# QA-SRS ClickHouse Operator FIPS 140-3
# Software Requirements Specification

(c) 2026 Altinity Inc. All Rights Reserved.

**Document status:** Confidential

**Author:** Saba Momtselidze

**Date:** May 29, 2026

## Table of Contents

* 1 [Introduction](#introduction)
* 2 [Configuration Requirements](#configuration-requirements)
    * 2.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Config.ExternalTLS](#rqsrs-026clickhouseoperatorfipsconfigexternaltls)
* 3 [Build Verification](#build-verification)
    * 3.1 [Shipped Binaries](#shipped-binaries)
        * 3.1.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Build.ShippedBinaries](#rqsrs026clickhouseoperatorfipsbuildshippedbinaries)
            * 3.1.1.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Build.ShippedBinaries.GOFIPS140](#rqsrs026clickhouseoperatorfipsbuildshippedbinariesgofips140)
            * 3.1.1.2 [RQ.SRS-026.ClickHouseOperator.FIPS.Build.ShippedBinaries.FIPSIdentity](#rqsrs026clickhouseoperatorfipsbuildshippedbinariesfipsidentity)
            * 3.1.1.3 [RQ.SRS-026.ClickHouseOperator.FIPS.Build.ShippedBinaries.FIPSVersion](#rqsrs026clickhouseoperatorfipsbuildshippedbinariesfipsversion)
            * 3.1.1.4 [RQ.SRS-026.ClickHouseOperator.FIPS.Build.ShippedBinaries.FIPSEnabled](#rqsrs026clickhouseoperatorfipsbuildshippedbinariesfipsenabled)
            * 3.1.1.5 [RQ.SRS-026.ClickHouseOperator.FIPS.Build.ShippedBinaries.StartupBanner](#rqsrs026clickhouseoperatorfipsbuildshippedbinariesstartupbanner)
* 4 [GODEBUG Strict Mode Smoke Test](#godebug-strict-mode-smoke-test)
    * 4.1 [RQ.SRS-026.ClickHouseOperator.FIPS.GODEBUG.StrictMode](#rqsrs-026clickhouseoperatorfipsgodebugstrictmode)
* 5 [FIPS 140-3 Valid TLS Cipher Suites](#fips-140-3-valid-tls-cipher-suites)
    * 5.1 [Approved TLS Cipher Suites](#approved-tls-cipher-suites)
        * 5.1.1 [RQ.SRS-026.ClickHouseOperator.FIPS.TLS.ApprovedCiphers](#rqsrs-026clickhouseoperatorfipstlsapprovedciphers)
    * 5.2 [Rejected Cipher Suites and Protocols](#rejected-cipher-suites-and-protocols)
        * 5.2.1 [RQ.SRS-026.ClickHouseOperator.FIPS.TLS.RejectedCiphers](#rqsrs-026clickhouseoperatorfipstlsrejectedciphers)
* 6 [ClickHouse Server and Keeper FIPS Configurations](#clickhouse-server-and-keeper-fips-configurations)
    * 6.1 [ClickHouse Server](#clickhouse-server)
        * 6.1.1 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.FIPSConfig](#rqsrs026clickhouseoperatorfipsdataplanechfipsconfig)
        * 6.1.2 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHIDeploy](#rqsrs026clickhouseoperatorfipsdataplanechideploy)
        * 6.1.3 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.NoPlainHTTP](#rqsrs026clickhouseoperatorfipsdataplanechnoplainhttp)
        * 6.1.4 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.NoPlainNative](#rqsrs026clickhouseoperatorfipsdataplanechnoplainnative)
        * 6.1.5 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.NoUnexpectedPorts](#rqsrs026clickhouseoperatorfipsdataplanechnounexpectedports)
        * 6.1.6 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.InternodeTLS](#rqsrs026clickhouseoperatorfipsdataplanechinternodetls)
        * 6.1.7 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.ScaleUp](#rqsrs026clickhouseoperatorfipsdataplanechscaleup)
        * 6.1.8 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.ScaleDown](#rqsrs026clickhouseoperatorfipsdataplanechscaledown)
        * 6.1.9 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.ConfigUpdate](#rqsrs026clickhouseoperatorfipsdataplanechconfigupdate)
    * 6.2 [ClickHouse Keeper](#clickhouse-keeper)
        * 6.2.1 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.FIPSConfig](#rqsrs026clickhouseoperatorfipsdataplanechkfipsconfig)
        * 6.2.2 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHKDeploy](#rqsrs026clickhouseoperatorfipsdataplanechkdeploy)
        * 6.2.3 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.NoPlainClientPort](#rqsrs026clickhouseoperatorfipsdataplanechknoplainclientport)
        * 6.2.4 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.NoUnexpectedPorts](#rqsrs026clickhouseoperatorfipsdataplanechknounexpectedports)
        * 6.2.5 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.RaftTLS](#rqsrs026clickhouseoperatorfipsdataplanechkrafttls)
        * 6.2.6 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.ScaleUp](#rqsrs026clickhouseoperatorfipsdataplanechkscaleup)
        * 6.2.7 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.ScaleDown](#rqsrs026clickhouseoperatorfipsdataplanechkscaledown)
        * 6.2.8 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.ConfigUpdate](#rqsrs026clickhouseoperatorfipsdataplanechkconfigupdate)
    * 6.3 [ClickHouse Backup Sidecar](#clickhouse-backup-sidecar)
        * 6.3.0 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.VersionString](#rqsrs026clickhouseoperatorfipsdataplanechversionstring)
        * 6.3.1 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.FIPSBinary](#rqsrs026clickhouseoperatorfipsdataplanebackupfipsbinary)
        * 6.3.2 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.GOFIPS140](#rqsrs026clickhouseoperatorfipsdataplanebackupgofips140)
        * 6.3.3 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.OnlyTLSPorts](#rqsrs026clickhouseoperatorfipsdataplanebackuponlytlsports)
        * 6.3.4 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.HTTPSAPI](#rqsrs026clickhouseoperatorfipsdataplanebackuphttpsapi)
        * 6.3.5 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.ClickHouseOverTLS](#rqsrs026clickhouseoperatorfipsdataplanebackupclickhouseovertls)
        * 6.3.6 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.RestoreRoundTrip](#rqsrs026clickhouseoperatorfipsdataplanebackuprestoreroundtrip)
        * 6.3.7 [RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.RemoteUploadTLS](#rqsrs026clickhouseoperatorfipsdataplanebackupremoteuploadtls)
* 7 [FIPS Enforcement Mode](#fips-enforcement-mode)
    * 7.1 [Security Coercion](#security-coercion)
        * 7.1.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.CoerceVerifyStrict](#rqsrs026clickhouseoperatorfipsenforcedcoerceverifystrict)
        * 7.1.2 [RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.CoerceMinVersion13](#rqsrs026clickhouseoperatorfipsenforcedcoerceminversion13)
        * 7.1.3 [RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.OverrideMinVersion12To13](#rqsrs-026clickhouseoperatorfipsenforcedoverrideminversion12to13)
        * 7.1.4 [RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.CoerceIPCSecure](#rqsrs026clickhouseoperatorfipsenforcedcoerceipcsecure)
        * 7.1.5 [RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectInsecureKubeconfig](#rqsrs026clickhouseoperatorfipsenforcedrejectinsecurekubeconfig)
        * 7.1.6 [RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectVerifyNoneCHI](#rqsrs026clickhouseoperatorfipsenforcedrejectverifynonechi)
        * 7.1.7 [RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectVerifyNoneZK](#rqsrs026clickhouseoperatorfipsenforcedrejectverifynonezk)
        * 7.1.8 [RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectInvalidMinVersion](#rqsrs026clickhouseoperatorfipsenforcedrejectinvalidminversion)
        * 7.1.9 [RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectExternalZookeeper](#rqsrs026clickhouseoperatorfipsenforcedrejectexternalzookeeper)
        * 7.1.10 [RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectCHKBypass](#rqsrs026clickhouseoperatorfipsenforcedrejectchkbypass)
    * 7.2 [Image Policy](#image-policy)
        * 7.2.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.RejectCHI](#rqsrs026clickhouseoperatorfipsimagesrequiredrejectchi)
        * 7.2.2 [RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.AcceptCHI](#rqsrs026clickhouseoperatorfipsimagesrequiredacceptchi)
        * 7.2.3 [RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.RejectCHK](#rqsrs026clickhouseoperatorfipsimagesrequiredrejectchk)
        * 7.2.4 [RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.RuntimeVersion](#rqsrs026clickhouseoperatorfipsimagesrequiredruntimeversion)
        * 7.2.5 [RQ.SRS-026.ClickHouseOperator.FIPS.Images.Permissive](#rqsrs026clickhouseoperatorfipsimagespermissive)
        * 7.2.6 [RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.ShortCircuit](#rqsrs026clickhouseoperatorfipsimagesrequiredshortcircuit)
    * 7.3 [Image Tag Detection](#image-tag-detection)
        * 7.3.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.FIPSSuffix](#rqsrs026clickhouseoperatorfipsimagestagdetectionfipssuffix)
        * 7.3.2 [RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.AltinityFIPS](#rqsrs026clickhouseoperatorfipsimagestagdetectionaltinityfips)
        * 7.3.3 [RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.DigestOnly](#rqsrs026clickhouseoperatorfipsimagestagdetectiondigestonly)
        * 7.3.4 [RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.RegistryPath](#rqsrs026clickhouseoperatorfipsimagestagdetectionregistrypath)
        * 7.3.5 [RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.CaseInsensitive](#rqsrs026clickhouseoperatorfipsimagestagdetectioncaseinsensitive)
* 8 [Operator External Connections](#operator-external-connections)
    * 8.1 [Operator Runtime Listener Verification](#operator-runtime-listener-verification)
        * 8.1.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.Listeners](#rqsrs026clickhouseoperatorfipsconnectoperatorlisteners)
    * 8.2 [Operator to Kubernetes API](#operator-to-kubernetes-api)
        * 8.2.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.Kubernetes](#rqsrs026clickhouseoperatorfipsconnectoperatorkubernetes)
    * 8.3 [Operator to ClickHouse Server](#operator-to-clickhouse-server)
        * 8.3.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.ClickHouse](#rqsrs026clickhouseoperatorfipsconnectoperatorclickhouse)
    * 8.4 [Operator to ZooKeeper/Keeper](#operator-to-zookeeperkeeper)
        * 8.4.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.Zookeeper](#rqsrs026clickhouseoperatorfipsconnectoperatorzookeeper)
    * 8.5 [Operator to metrics-exporter IPC](#operator-to-metrics-exporter-ipc)
        * 8.5.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.IPCSecure](#rqsrs026clickhouseoperatorfipsconnectoperatoripcsecure)
    * 8.6 [Operator Prometheus Metrics](#operator-prometheus-metrics)
        * 8.6.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Gap.OperatorMetricsTLS](#rqsrs026clickhouseoperatorfipsgapoperatormetricstls)
* 9 [Exporter External Connections](#exporter-external-connections)
    * 9.1 [Exporter Runtime Listener Verification](#exporter-runtime-listener-verification)
        * 9.1.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Exporter.Listeners](#rqsrs026clickhouseoperatorfipsconnectexporterlisteners)
    * 9.2 [Exporter to Kubernetes API](#exporter-to-kubernetes-api)
        * 9.2.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Exporter.Kubernetes](#rqsrs026clickhouseoperatorfipsconnectexporterkubernetes)
    * 9.3 [Exporter to ClickHouse Server](#exporter-to-clickhouse-server)
        * 9.3.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Exporter.ClickHouse](#rqsrs026clickhouseoperatorfipsconnectexporterclickhouse)
    * 9.4 [Exporter Prometheus Metrics](#exporter-prometheus-metrics)
        * 9.4.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Gap.ExporterMetricsTLS](#rqsrs026clickhouseoperatorfipsgapexportermetricstls)
* 10 [Integrity Check Failure](#integrity-check-failure)
    * 10.1 [Operator Integrity Tampering](#operator-integrity-tampering)
        * 10.1.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Integrity.OperatorMismatch](#rqsrs026clickhouseoperatorfipsintegrityoperatormismatch)
    * 10.2 [Exporter Integrity Tampering](#exporter-integrity-tampering)
        * 10.2.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Integrity.ExporterMismatch](#rqsrs026clickhouseoperatorfipsintegrityexportermismatch)
* 11 [CAST Failure](#cast-failure)
    * 11.1 [Operator CAST Failure](#operator-cast-failure)
        * 11.1.1 [RQ.SRS-026.ClickHouseOperator.FIPS.CAST.OperatorFail](#rqsrs026clickhouseoperatorfipscastoperatorfail)
    * 11.2 [Exporter CAST Failure](#exporter-cast-failure)
        * 11.2.1 [RQ.SRS-026.ClickHouseOperator.FIPS.CAST.ExporterFail](#rqsrs026clickhouseoperatorfipscastexporterfail)
* 12 [Synthetic TLS Cipher Validation](#synthetic-tls-cipher-validation)
    * 12.1 [Approved cipher matrix](#approved-cipher-matrix)
        * 12.1.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Synthetic.ApprovedCiphers](#rqsrs-026clickhouseoperatorfipssyntheticapprovedciphers)
    * 12.2 [Rejected cipher matrix](#rejected-cipher-matrix)
        * 12.2.1 [RQ.SRS-026.ClickHouseOperator.FIPS.Synthetic.RejectedCiphers](#rqsrs-026clickhouseoperatorfipssyntheticrejectedciphers)
* 13 [CI/CD Image and Policy Verification](#cicd-image-and-policy-verification)
    * 13.1 [RQ.SRS-026.ClickHouseOperator.FIPS.CICD.OperatorImageBuild](#rqsrs-026clickhouseoperatorfipscicdoperatorimagebuild)
    * 13.2 [RQ.SRS-026.ClickHouseOperator.FIPS.CICD.ExporterImageBuild](#rqsrs-026clickhouseoperatorfipscicdexporterimagebuild)
    * 13.3 [RQ.SRS-026.ClickHouseOperator.FIPS.CICD.VulnerabilityScan](#rqsrs-026clickhouseoperatorfipscicdvulnerabilityscan)
* 14 [AI Static Code Review](#ai-static-code-review)
    * 14.1 [Operator Source Review](#operator-source-review)
        * 14.1.1 [RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Operator.Tree](#rqsrs-026clickhouseoperatorfipsaireviewoperatortree)
        * 14.1.2 [RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Operator.SharedPkg](#rqsrs-026clickhouseoperatorfipsaireviewoperatorsharedpkg)
        * 14.1.3 [RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Operator.RegressionGate](#rqsrs-026clickhouseoperatorfipsaireviewoperatorregressiongate)
    * 14.2 [Exporter Source Review](#exporter-source-review)
        * 14.2.1 [RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Exporter.Tree](#rqsrs-026clickhouseoperatorfipsaireviewexportertree)
        * 14.2.2 [RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Exporter.SharedPkg](#rqsrs-026clickhouseoperatorfipsaireviewexportersharedpkg)
        * 14.2.3 [RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Exporter.RegressionGate](#rqsrs-026clickhouseoperatorfipsaireviewexporterregressiongate)
* 15 [ACVP Algorithm Validation](#acvp-algorithm-validation)
    * 15.1 [Operator ACVP Validation](#operator-acvp-validation)
        * 15.1.1 [RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.WrapperIntegration](#rqsrs026clickhouseoperatorfipsacvpoperatorwrapperintegration)
        * 15.1.2 [RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.ConfigGeneration](#rqsrs026clickhouseoperatorfipsacvpoperatorconfiggeneration)
        * 15.1.3 [RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.ExpectedOutputReplay](#rqsrs026clickhouseoperatorfipsacvpoperatorexpectedoutputreplay)
        * 15.1.4 [RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.SuiteCount](#rqsrs026clickhouseoperatorfipsacvpoperatorsuitecount)
    * 15.2 [Exporter ACVP Validation](#exporter-acvp-validation)
        * 15.2.1 [RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.WrapperIntegration](#rqsrs026clickhouseoperatorfipsacvpexporterwrapperintegration)
        * 15.2.2 [RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.ConfigGeneration](#rqsrs026clickhouseoperatorfipsacvpexporterconfiggeneration)
        * 15.2.3 [RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.ExpectedOutputReplay](#rqsrs026clickhouseoperatorfipsacvpexporterexpectedoutputreplay)
        * 15.2.4 [RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.SuiteCount](#rqsrs026clickhouseoperatorfipsacvpexportersuitecount)
* 16 [Terminology](#terminology)
    * 16.1 [SRS](#srs)
    * 16.2 [FIPS 140-3](#fips-140-3)
    * 16.3 [clickhouse-operator](#clickhouse-operator)
    * 16.4 [metrics-exporter](#metrics-exporter)
    * 16.5 [CHI](#chi)
    * 16.6 [CHK](#chk)
    * 16.7 [ACVP](#acvp)
    * 16.8 [CMVP](#cmvp)
    * 16.9 [CAVP](#cavp)

## Introduction

This specification describes FIPS 140-3 compatibility requirements for the
[clickhouse-operator] and [metrics-exporter] binaries built with Go FIPS support.

The goal is to verify that FIPS-enabled builds of the operator and metrics-exporter:
- Operate correctly under FIPS constraints
- Properly enforce cryptographic restrictions
- Use FIPS-compliant TLS for all inbound and outbound connections

Autotests that trace to these requirements live in
[`tests/e2e/test_operator_fips.py`](../e2e/test_operator_fips.py) and
[`tests/e2e/test_acvp.py`](../e2e/test_acvp.py).

**Boundary:** The operator and metrics-exporter run in the same pod. Internal IPC between
them is localhost HTTP and is not subject to FIPS TLS requirements. The Prometheus metrics
endpoints (operator `:9999` and metrics-exporter `:8888`) are also served over plain HTTP
and remain outside the FIPS TLS scope as a known gap.

## Configuration Requirements

Plain HTTP/TCP on any external connection is a configuration error for FIPS compliance.
TLS must be enabled for all connections to:

- Kubernetes API
- ClickHouse Server
- ZooKeeper/Keeper
- Prometheus scrape endpoints

### RQ.SRS-026.ClickHouseOperator.FIPS.Config.ExternalTLS
version: 1.0

Plain HTTP/TCP on external connections SHALL be treated as a configuration error for FIPS compliance. TLS SHALL be enabled for connections to the [Kubernetes API], [ClickHouse Server], [ZooKeeper/Keeper], and Prometheus scrape endpoints.

## Build Verification

**Objective:** Verify each shipped binary is a FIPS build and linked to Go Cryptographic Module v1.0.0.

**Certificates:**
- [CMVP #5247](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/5247)
- [CAVP A6650](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/details?product=19371)

**Build requirement:** `GOFIPS140=v1.0.0` (or `certified`)


### Shipped Binaries

#### RQ.SRS-026.ClickHouseOperator.FIPS.Build.ShippedBinaries
version: 1.0

Each shipped pod binary — `clickhouse-operator` and `metrics-exporter` — SHALL satisfy all of the following:

* Both binaries SHALL be built with `GOFIPS140=v1.0.0` (or `certified`); `go version -m` on each binary SHALL show the `GOFIPS140` build setting when the binary is inspectable.
* Each binary SHALL identify itself as a FIPS build via `--version` output, `--fips-info`, or startup logs containing a FIPS indicator.
* Each binary SHALL report `crypto/fips140.Version()` equal to `v1.0.0` (for example via `--fips-info` or in-process inspection).
* Each binary SHALL report `crypto/fips140.Enabled()` equal to `true` when FIPS mode is active per `GODEBUG=fips140`.

Examples:
* `go version -m clickhouse-operator` contains `GOFIPS140=v1.0.0`
* `go version -m metrics-exporter` contains `GOFIPS140=v1.0.0`
* `clickhouse-operator --fips-info` reports:

  ```yaml
  fips_module:
    version: v1.0.0
    enabled: true
  ```

* `metrics-exporter --fips-info` reports:

  ```yaml
  fips_module:
    version: v1.0.0
    enabled: true
  ```

#### RQ.SRS-026.ClickHouseOperator.FIPS.Build.ShippedBinaries.StartupLogs
version: 1.0

At startup, each binary SHALL emit a FIPS startup banner in logs indicating build and runtime FIPS state.

when GODEBUG=fips140=only:

```text
FIPS: chopconf.fips.enforced=true \
build.linked=true \
module.active=true \
runtime.enforced=true \
module=v1.0.0
```



## Approved TLS Cipher Suites

### RQ.SRS-026.ClickHouseOperator.FIPS.TLS.ApprovedCiphers
version: 1.0

TLS-enforced external connections for [clickhouse-operator] and [metrics-exporter]
SHALL negotiate only TLS 1.3 with the following approved cipher suites.

| Cipher Suite | OpenSSL Name |
|--------------|--------------|
| TLS_AES_128_GCM_SHA256 | TLS_AES_128_GCM_SHA256 |
| TLS_AES_256_GCM_SHA384 | TLS_AES_256_GCM_SHA384 |
| TLS_AES_128_CCM_SHA256 | TLS_AES_128_CCM_SHA256 |
| TLS_AES_128_CCM_8_SHA256 | TLS_AES_128_CCM_8_SHA256 |

### Rejected Cipher Suites and Protocols

#### RQ.SRS-026.ClickHouseOperator.FIPS.TLS.RejectedCiphers
version: 1.0

TLS connections SHALL reject the following for all TLS-enabled external connections:

- Any TLS cipher suite not explicitly listed in [RQ.SRS-026.ClickHouseOperator.FIPS.TLS.ApprovedCiphers](#rqsrs-026clickhouseoperatorfipstlsapprovedciphers)
- Protocol versions: SSLv2, SSLv3, TLS 1.0, TLS 1.1
- Cipher suites using non-approved/legacy algorithms (for this profile), including:
  - ChaCha20-Poly1305
  - RC4, RC2, DES, 3DES, IDEA, SEED, CAMELLIA, ARIA
  - NULL encryption / NULL authentication
  - Anonymous key exchange (`aNULL`, `eNULL`, `ADH`, `AECDH`)
  - Export/weak suites (`EXP`, `LOW`, `40-bit`, `56-bit`)
  - MD5- or SHA-1-based legacy suites


## ClickHouse Server and Keeper FIPS Configurations

**Objective:** Verify the operator generates and maintains FIPS-compliant configurations for ClickHouse servers and Keepers.


### ClickHouse Server

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.FIPSConfig
version: 1.0

Deploying a CHI with FIPS TLS settings SHALL start ClickHouse with FIPS-compliant TLS configuration.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHIDeploy
version: 1.0

The operator SHALL deploy FIPS `ClickHouseInstallation` resources to `Completed` with Running pods when configuration is valid.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.NoPlainHTTP
version: 1.0

When FIPS transport hardening applies, ClickHouse pods SHALL NOT listen on plain HTTP port 8123; HTTPS port 8443 SHALL be used.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.NoPlainNative
version: 1.0

When FIPS transport hardening applies, ClickHouse pods SHALL NOT listen on plain native TCP port 9000; secure native port 9440 SHALL be used.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.NoUnexpectedPorts
version: 1.0

ClickHouse pods in a FIPS deployment SHALL expose only expected secure listener ports and no additional unexpected ports.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.InternodeTLS
version: 1.0

ReplicatedMergeTree replicas SHALL communicate over interserver HTTPS (`interserver_https_port`) and data SHALL converge across replicas.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.ScaleUp
version: 1.0

Adding a replica to a FIPS-configured CHI SHALL reconcile to `Completed` and the new replica SHALL run the FIPS ClickHouse binary with TLS-only listeners.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.ScaleDown
version: 1.0

Removing a replica from a FIPS-configured CHI SHALL reconcile to `Completed` and remaining replicas SHALL keep FIPS binary and TLS-only configuration.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.ConfigUpdate
version: 1.0

Updating TLS settings on a running CHI SHALL reload ClickHouse with the new FIPS-compliant configuration.


### ClickHouse Keeper

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.FIPSConfig
version: 1.0

Deploying a CHK with FIPS TLS settings SHALL start Keeper with FIPS-compliant TLS configuration.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHKDeploy
version: 1.0

The operator SHALL deploy FIPS `ClickHouseKeeperInstallation` resources to `Completed` with Running pods when configuration is valid.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.NoPlainClientPort
version: 1.0

When FIPS transport hardening applies, Keeper pods SHALL NOT listen on plain client port 2181; secure client port 2281 SHALL be used.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.NoUnexpectedPorts
version: 1.0

Keeper pods in a FIPS deployment SHALL expose only expected secure listener ports.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.RaftTLS
version: 1.0

Keeper Raft communication SHALL use TLS on the configured secure Raft port.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.ScaleUp
version: 1.0

Adding a node to a FIPS-configured Keeper cluster SHALL reconcile to `Completed` and the new node SHALL run the FIPS Keeper binary with TLS-only client and Raft listeners.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.ScaleDown
version: 1.0

Removing a node from a FIPS-configured Keeper cluster SHALL reconcile to `Completed` and remaining nodes SHALL keep FIPS configuration.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CHK.ConfigUpdate
version: 1.0

Updating TLS settings on a running CHK SHALL reload Keeper with the new FIPS-compliant configuration.


### ClickHouse Backup Sidecar

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.CH.VersionString
version: 1.0

A running ClickHouse host under FIPS image policy SHALL report a `version()` string containing `fips` (case-insensitive).

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.FIPSBinary
version: 1.0

The `clickhouse-backup` sidecar SHALL run a FIPS-built binary; `clickhouse-backup --version` SHALL contain `fips` (case-insensitive).

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.GOFIPS140
version: 1.0

When inspectable, the clickhouse-backup sidecar binary SHALL embed `GOFIPS140=v1.0.0` per `go version -m`.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.OnlyTLSPorts
version: 1.0

The clickhouse-backup sidecar SHALL expose only secure listener ports (including HTTPS API port 7171).

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.HTTPSAPI
version: 1.0

The clickhouse-backup HTTPS API SHALL serve over TLS with CA-trust enforcement: trusted clients accepted, untrusted clients rejected.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.ClickHouseOverTLS
version: 1.0

The clickhouse-backup sidecar SHALL reach ClickHouse over secure native TCP.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.RestoreRoundTrip
version: 1.0

Backup and restore through the HTTPS API SHALL succeed over TLS.

#### RQ.SRS-026.ClickHouseOperator.FIPS.DataPlane.Backup.RemoteUploadTLS
version: 1.0

Remote backup upload to object storage SHALL use FIPS-approved TLS.


## FIPS Enforcement Mode

**Objective:** Verify `security.fips.enforced=true` coerces security settings and rejects non-compliant configurations.


### Security Coercion

#### RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.CoerceVerifyStrict
version: 1.0

With `fips.enforced=true`, unset TLS verify SHALL be coerced to Strict for ClickHouse, ZooKeeper/Keeper, and Kubernetes clients.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.CoerceMinVersion13
version: 1.0

With `fips.enforced=true`, unset TLS minVersion SHALL be coerced to 1.3 for the
operator's outbound TLS clients.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.OverrideMinVersion12To13
version: 1.0

When `security.fips.enforced: "true"` is set in the [ClickHouseOperatorConfiguration], the operator SHALL coerce `minVersion` to `"1.3"` for `security.clickhouse.tls`, `security.zookeeper.tls`, and `security.kubernetes.tls`, even when those fields are explicitly set to `"1.2"`.

```yaml
spec:
  security:
    fips:
      enforced: "true"
    clickhouse:
      tls:
        minVersion: "1.2"
    zookeeper:
      tls:
        minVersion: "1.2"
    kubernetes:
      tls:
        minVersion: "1.2"
```

After operator configuration normalization, the effective `minVersion` for each component listed above SHALL be `"1.3"`.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.CoerceIPCSecure
version: 1.0

With `fips.enforced=true`, unset IPC mode SHALL be coerced to Secure.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectInsecureKubeconfig
version: 1.0

The operator SHALL refuse to start when kubeconfig uses `TLSClientConfig.Insecure=true` under strict/FIPS mode.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectVerifyNoneCHI
version: 1.0

CHI with `clickhouse.tls.verify=None` under enforced mode SHALL be rejected with `FIPSValidationFailed`.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectVerifyNoneZK
version: 1.0

CHI with `zookeeper.tls.verify=None` under enforced mode SHALL be rejected.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectInvalidMinVersion
version: 1.0

CHI with invalid TLS minVersion under enforced mode SHALL be rejected.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectExternalZookeeper
version: 1.0

CHI referencing plain external ZooKeeper nodes under enforced mode SHALL be rejected.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.RejectCHKBypass
version: 1.0

CHK with TLS verify bypass under enforced mode SHALL be rejected.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Enforced.MinVersionScope
version: 1.0

The `minVersion` coercion SHALL apply only to TLS clients created and managed by the operator.
They SHALL NOT require ClickHouse Server or ClickHouse Keeper listener endpoints to reject TLS 1.2.

### Image Policy

#### RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.RejectCHI
version: 1.0

With `security.fips.images.policy=Required`, CHI with non-FIPS image tag SHALL be rejected with `FIPSImagePolicyViolation`.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.AcceptCHI
version: 1.0

With image policy Required, CHI with FIPS-tagged image SHALL reconcile normally.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.RejectCHK
version: 1.0

With image policy Required, CHK with non-FIPS Keeper image SHALL be rejected.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.RuntimeVersion
version: 1.0

With image policy Required, host `SELECT version()` lacking `fips` SHALL fail with `FIPSImagePolicyViolation`.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Images.Permissive
version: 1.0

With permissive image policy, non-FIPS CHI images SHALL reconcile (default).

#### RQ.SRS-026.ClickHouseOperator.FIPS.Images.Required.ShortCircuit
version: 1.0

Multiple non-FIPS hosts SHALL produce a single policy violation error.


### Image Tag Detection

#### RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.FIPSSuffix
version: 1.0

Image tags containing `fips` (case-insensitive) SHALL be detected as FIPS.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.AltinityFIPS
version: 1.0

Image tags containing `altinityfips` SHALL be detected as FIPS.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.DigestOnly
version: 1.0

Digest-only image references SHALL NOT be detected as FIPS at admission.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.RegistryPath
version: 1.0

Registry hostname containing `fips` SHALL NOT satisfy FIPS tag detection.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Images.TagDetection.CaseInsensitive
version: 1.0

Image tags such as `25.3.FIPS` or `25.3.Fips` SHALL be detected as FIPS (case-insensitive match on the tag).


## Operator External Connections

**Objective:** Verify all **clickhouse-operator** inbound and outbound connections use FIPS-compliant TLS.


### Operator Runtime Listener Verification

In a FIPS deployment, workload containers deployed by the operator (ClickHouse, Keeper, and sidecar containers) SHALL expose only expected TLS listener ports. Verification reads `/proc/net/tcp` and `/proc/net/tcp6` inside each container and parses ports in LISTEN state (`0A`):

```bash
kubectl exec <pod> -c clickhouse -- sh -c 'cat /proc/net/tcp /proc/net/tcp6'
```

E2e coverage: [`test_020011`](../e2e/test_operator_fips.py#L200).

#### RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.Listeners
version: 1.0

FIPS workload pods (ClickHouse, Keeper, and sidecar containers) SHALL listen only on expected TLS ports. Plaintext service ports (8123, 9000, 2181) SHALL NOT be open when FIPS transport hardening applies.


### Operator to Kubernetes API

#### RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.Kubernetes
version: 1.0

The operator SHALL connect to the Kubernetes API using FIPS-approved TLS ciphers.


### Operator to ClickHouse Server

#### RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.ClickHouse
version: 1.0

The operator SHALL connect to ClickHouse using FIPS-approved TLS ciphers.


### Operator to ZooKeeper/Keeper

#### RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.Zookeeper
version: 1.0

The operator SHALL connect to ZooKeeper/Keeper using FIPS-approved TLS ciphers.


### Operator to metrics-exporter IPC

#### RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Operator.IPCSecure
version: 1.0

Operator IPC with `security.ipc.mode=Secure` SHALL work over localhost HTTP with token auth.


### Operator Prometheus Metrics

#### RQ.SRS-026.ClickHouseOperator.FIPS.Gap.OperatorMetricsTLS
version: 1.0

Operator Prometheus metrics on :9999 currently expose a known FIPS gap (HTTP-only).


## Exporter External Connections

**Objective:** Verify all **metrics-exporter** inbound and outbound connections use FIPS-compliant TLS.


### Exporter Runtime Listener Verification

Listener audits use the same `/proc/net/tcp` technique as [Operator Runtime Listener Verification](#operator-runtime-listener-verification). E2e audits the **clickhouse-backup** sidecar in [`test_020011`](../e2e/test_operator_fips.py#L200). The **metrics-exporter** process on `:8888` remains a known gap until metrics TLS is implemented.

#### RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Exporter.Listeners
version: 1.0

The metrics-exporter process SHALL expose only expected listener ports on `:8888`. Sidecar containers in the same pod SHALL be listener-audited with the same `/proc/net/tcp` procedure.


### Exporter to Kubernetes API

#### RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Exporter.Kubernetes
version: 1.0

The exporter SHALL connect to the Kubernetes API using FIPS-approved TLS ciphers.


### Exporter to ClickHouse Server

#### RQ.SRS-026.ClickHouseOperator.FIPS.Connect.Exporter.ClickHouse
version: 1.0

The exporter SHALL query ClickHouse using FIPS-approved TLS when configured for HTTPS.


### Exporter Prometheus Metrics

#### RQ.SRS-026.ClickHouseOperator.FIPS.Gap.ExporterMetricsTLS
version: 1.0

Exporter Prometheus metrics on :8888 currently expose a known FIPS gap (HTTP-only).


## Integrity Check Failure

**Objective:** Verify FIPS integrity self-test detects binary tampering for each shipped binary independently.


### Operator Integrity Tampering

#### RQ.SRS-026.ClickHouseOperator.FIPS.Integrity.OperatorMismatch
version: 1.0

Tampering with `clickhouse-operator` `.go.fipsinfo` SHALL panic with `fips140: verification mismatch`.


### Exporter Integrity Tampering

#### RQ.SRS-026.ClickHouseOperator.FIPS.Integrity.ExporterMismatch
version: 1.0

Tampering with `metrics-exporter` `.go.fipsinfo` SHALL panic with `fips140: verification mismatch`.


## CAST Failure

**Objective:** Verify FIPS Cryptographic Algorithm Self-Test (CAST) detects failures in each binary independently.


### Operator CAST Failure

#### RQ.SRS-026.ClickHouseOperator.FIPS.CAST.OperatorFail
version: 1.0

Running `clickhouse-operator` with `GODEBUG=failfipscast=<name>` SHALL terminate with a CAST error.


### Exporter CAST Failure

#### RQ.SRS-026.ClickHouseOperator.FIPS.CAST.ExporterFail
version: 1.0

Running `metrics-exporter` with `GODEBUG=failfipscast=<name>` SHALL terminate with a CAST error.


## Synthetic TLS Cipher Validation

**Objective:** Validate FIPS cipher enforcement on all external (to the pod) connections using `openssl s_client` and `openssl s_server`.

Use `openssl` to simulate connections with specific ciphers and verify the operator/exporter accepts FIPS-approved ciphers and rejects non-approved ones.

```bash
# Operator as TLS client against server offering only approved cipher
openssl s_server -accept 8443 -cert server.crt -key server.key \
  -ciphersuites TLS_AES_256_GCM_SHA384

# Operator as TLS client against server offering non-approved cipher
openssl s_server -accept 8443 -cert server.crt -key server.key \
  -cipher ECDHE-RSA-CHACHA20-POLY1305

# Inbound connection to operator/exporter metrics endpoint
openssl s_client -connect localhost:9999 -cipher ECDHE-RSA-AES256-GCM-SHA384
```

### Approved cipher matrix

#### RQ.SRS-026.ClickHouseOperator.FIPS.Synthetic.ApprovedCiphers
version: 1.0

For each external connection listed below, when exercised as a TLS **client** with `openssl s_server` offering only [approved ciphers](#rqsrs-026clickhouseoperatorfipstlsapprovedciphers), or as a TLS **server** with `openssl s_client` using only approved ciphers, the connection SHALL succeed:

| Connection | Role | Tool |
|------------|------|------|
| Operator to Kubernetes API | Client | `openssl s_server` |
| Operator to ClickHouse Server | Client | `openssl s_server` |
| Operator to ZooKeeper/Keeper | Client | `openssl s_server` |
| Operator metrics :9999 | Server | `openssl s_client` |
| Exporter to Kubernetes API | Client | `openssl s_server` |
| Exporter to ClickHouse Server | Client | `openssl s_server` |
| Exporter metrics :8888 | Server | `openssl s_client` |


### Rejected cipher matrix

#### RQ.SRS-026.ClickHouseOperator.FIPS.Synthetic.RejectedCiphers
version: 1.0

For each external connection listed below, when the peer offers only [rejected ciphers or protocols](#rqsrs-026clickhouseoperatorfipstlsrejectedciphers), the connection SHALL be rejected:

| Connection | Role | Tool |
|------------|------|------|
| Operator to Kubernetes API | Client | `openssl s_server` |
| Operator to ClickHouse Server | Client | `openssl s_server` |
| Operator to ZooKeeper/Keeper | Client | `openssl s_server` |
| Operator metrics :9999 | Server | `openssl s_client` |
| Exporter to Kubernetes API | Client | `openssl s_server` |
| Exporter to ClickHouse Server | Client | `openssl s_server` |
| Exporter metrics :8888 | Server | `openssl s_client` |


## CI/CD Image and Policy Verification

**Objective:** Add CI/CD jobs to validate FIPS image build and supply-chain checks.

### RQ.SRS-026.ClickHouseOperator.FIPS.CICD.OperatorImageBuild
version: 1.0

CI SHALL build the [clickhouse-operator] FIPS image successfully.

### RQ.SRS-026.ClickHouseOperator.FIPS.CICD.ExporterImageBuild
version: 1.0

CI SHALL build the [metrics-exporter] FIPS image successfully.

### RQ.SRS-026.ClickHouseOperator.FIPS.CICD.VulnerabilityScan
version: 1.0

FIPS images SHALL pass vulnerability scanning with no Critical, High, or Medium findings.


### Operator Source Review

#### RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Operator.Tree
version: 1.0

Static review of operator-scoped paths SHALL produce no Critical findings; Warning-level findings SHALL be documented.

#### RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Operator.SharedPkg
version: 1.0

Review of shared packages reachable from `cmd/operator` SHALL produce no Critical findings.

#### RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Operator.RegressionGate
version: 1.0

A signed-off review artifact SHALL be stored with the build record before release.

### Exporter Source Review

#### RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Exporter.Tree
version: 1.0

Static review of exporter-scoped paths SHALL produce no Critical findings; Warning-level findings SHALL be documented.

#### RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Exporter.SharedPkg
version: 1.0

Review of shared packages reachable from `cmd/metrics_exporter` SHALL produce no Critical findings.

#### RQ.SRS-026.ClickHouseOperator.FIPS.AIReview.Exporter.RegressionGate
version: 1.0

A signed-off review artifact SHALL be stored with the build record before release.

## ACVP Algorithm Validation

**Objective:** Reproduce ACVP expected-output checks for each FIPS binary using the tracked public-scope config in [`pkg/util/fips/acvp/`](../../../pkg/util/fips/acvp/).


### Operator ACVP Validation

#### RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.WrapperIntegration
version: 1.0

Building clickhouse-operator with `-tags acvp_wrapper` SHALL expose a working ACVP responder via argv0 dispatch.

#### RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.ConfigGeneration
version: 1.0

The clickhouse-operator ACVP responder SHALL answer `getConfig` with supported capabilities.

#### RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.ExpectedOutputReplay
version: 1.0

`bash pkg/util/fips/acvp/run.sh` SHALL match all configured expected outputs for the operator.

#### RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Operator.SuiteCount
version: 1.0

The tracked ACVP config SHALL report 38 matched expectations for clickhouse-operator.


### Exporter ACVP Validation

#### RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.WrapperIntegration
version: 1.0

Building metrics-exporter with `-tags acvp_wrapper` SHALL expose a working ACVP responder.

#### RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.ConfigGeneration
version: 1.0

The metrics-exporter ACVP responder SHALL answer `getConfig` with supported capabilities.

#### RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.ExpectedOutputReplay
version: 1.0

`BINARY=metrics-exporter bash pkg/util/fips/acvp/run.sh` SHALL match all expected outputs.

#### RQ.SRS-026.ClickHouseOperator.FIPS.ACVP.Exporter.SuiteCount
version: 1.0

The tracked ACVP config SHALL report 38 matched expectations for metrics-exporter.

## Terminology

### SRS

Software Requirements Specification.

### FIPS 140-3

Federal Information Processing Standard for cryptographic module validation.

### clickhouse-operator

The Altinity ClickHouse Operator Kubernetes controller binary.

### metrics-exporter

The Prometheus metrics exporter sidecar binary shipped in the operator pod.

### CHI

ClickHouseInstallation custom resource.

### CHK

ClickHouseKeeperInstallation custom resource.

### ACVP

Automated Cryptographic Validation Protocol.

### CMVP

Cryptographic Module Validation Program.

### CAVP

Cryptographic Algorithm Validation Program.

[clickhouse-operator]: #clickhouse-operator
[metrics-exporter]: #metrics-exporter
[Kubernetes API]: https://kubernetes.io/docs/reference/kubernetes-api/
[ClickHouse Server]: #clickhouse-server
[ZooKeeper/Keeper]: #clickhouse-keeper
'''
)
