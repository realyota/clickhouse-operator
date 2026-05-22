#!/bin/bash

# Build configuration options

CUR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
# All sources root
SRC_ROOT="$(realpath "${CUR_DIR}/..")"

# Deploy manifests root
MANIFESTS_ROOT="${SRC_ROOT}/deploy"
# Executable commands sources root
CMD_ROOT="${SRC_ROOT}/cmd"
# Packages root
PKG_ROOT="${SRC_ROOT}/pkg"

REPO="github.com/altinity/clickhouse-operator"

# 0.9.3
VERSION=$(cd "${SRC_ROOT}"; cat release)
# 885c3f7
GIT_SHA=$(cd "${SRC_ROOT}"; git rev-parse --short HEAD)
# 2020-03-07 14:54:56
NOW=$(date "+%FT%T")
# Which version of golang to use. Ex.: 1.23.0
GO_VERSION=$(cd "${SRC_ROOT}"; grep '^go ' go.mod | awk '{print $2}')

# Go FIPS 140-3 module version. Setting GOFIPS140 at build time links the Go
# FIPS 140-3 cryptographic module (`crypto/fips140` v1.0.0, currently in CMVP
# review — not yet a completed CMVP validation). Default runtime mode for
# GOFIPS140-built binaries is `GODEBUG=fips140=on` (TLS filtering). Strict
# mode `=only` is opt-in via the separate `:<version>-fips` image variant.
# Pass GOFIPS140= (empty) to disable for local non-FIPS builds.
#
# Avoid GOFIPS140=latest for ship builds — `latest` uses the toolchain's
# in-tree module rather than the frozen snapshot, defeating the reproducibility
# guarantee that the operator's FIPS-compatibility claim relies on. Always pin
# to the explicit version (e.g. v1.0.0).
GOFIPS140="${GOFIPS140-v1.0.0}"

RELEASE="1"

# Operator binary name can be specified externally
# Default - put 'clickhouse-operator' into cur dir
OPERATOR_BIN="${OPERATOR_BIN:-"${SRC_ROOT}/dev/bin/clickhouse-operator"}"

# Metrics exporter binary name can be specified externally
# Default - put 'metrics-exporter' into cur dir
METRICS_EXPORTER_BIN="${METRICS_EXPORTER_BIN:-"${SRC_ROOT}/dev/bin/metrics-exporter"}"
