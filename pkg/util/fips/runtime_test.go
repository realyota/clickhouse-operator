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

package fips

import (
	"testing"

	"github.com/stretchr/testify/require"
)

// TestRuntime_Stubbable verifies the indirection — production callers see
// crypto/fips140.{Enabled,Enforced}; tests swap the function-pointer pair to
// drive the gate decision matrix without depending on the actual Go toolchain
// FIPS posture (which a unit-test runner cannot control).
func TestRuntime_Stubbable(t *testing.T) {
	origEnabled, origEnforced := Enabled, Enforced
	t.Cleanup(func() { Enabled, Enforced = origEnabled, origEnforced })

	for _, want := range []bool{true, false} {
		Enabled = func() bool { return want }
		Enforced = func() bool { return !want }
		require.Equal(t, want, Enabled(), "Enabled stub")
		require.Equal(t, !want, Enforced(), "Enforced stub")
	}
}
