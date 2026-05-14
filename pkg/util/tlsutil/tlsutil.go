// Copyright 2019 Altinity Ltd and/or its affiliates. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package tlsutil

import (
	"crypto/tls"

	api "github.com/altinity/clickhouse-operator/pkg/apis/clickhouse.altinity.com/v1"
)

// VersionUint16 maps the typed TLSMinVersion ("1.2"|"1.3"|"") to the
// corresponding tls.Version* constant. Empty or unknown returns 0, which Go
// treats as "use the stdlib default" (currently 1.2). Shared by the ClickHouse
// and ZooKeeper client paths so both apply identical floor logic.
func VersionUint16(v api.TLSMinVersion) uint16 {
	switch v {
	case api.TLSMinVersion12:
		return tls.VersionTLS12
	case api.TLSMinVersion13:
		return tls.VersionTLS13
	default:
		return 0
	}
}
