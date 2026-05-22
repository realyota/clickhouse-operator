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

package util

import (
	"testing"

	"github.com/stretchr/testify/require"
)

// TestHashIntoString pins the externally-visible contract of HashIntoString:
// 40-char lowercase hex output (K8s label-value-safe; ≤63 chars rule), empty
// input returns empty, and the function is deterministic. The 40-char width
// is load-bearing — the output is written to
// `clickhouse.altinity.com/object-version` labels via MakeObjectVersion, and
// a width change would invalidate every label-value comparison across an
// operator upgrade. Failing this test means the algorithm has been swapped
// to a different hash or truncation length: review the K8s-label-width
// implication before touching.
func TestHashIntoString(t *testing.T) {
	require.Equal(t, "", HashIntoString(nil), "empty input must return empty string")
	require.Equal(t, "", HashIntoString([]byte{}), "zero-length input must return empty string")

	out := HashIntoString([]byte("any non-empty input"))
	require.Len(t, out, 40, "output width is part of the contract — K8s label values must be ≤63")
	require.Regexp(t, "^[0-9a-f]{40}$", out, "output must be lowercase hex")

	// Determinism.
	require.Equal(t, out, HashIntoString([]byte("any non-empty input")))

	// Different inputs produce different outputs.
	require.NotEqual(t, out, HashIntoString([]byte("another input")))
}
