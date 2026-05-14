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

package v1

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/require"

	"github.com/altinity/clickhouse-operator/pkg/apis/common/types"
)

// TestFIPS_IsEnforced_NilSafe verifies the nil-safe predicate at every
// reachable nil-shape: nil receiver, nil Enforced pointer, unset Enforced value,
// explicit false, explicit true. Matches the IPCMode.GetMode() shape.
func TestFIPS_IsEnforced_NilSafe(t *testing.T) {
	require.False(t, (*OperatorConfigSecurityFIPS)(nil).IsEnforced(), "nil receiver must report false")
	require.False(t, (&OperatorConfigSecurityFIPS{}).IsEnforced(), "unset Enforced must report false")
	require.False(t, (&OperatorConfigSecurityFIPS{Enforced: types.NewStringBool(false)}).IsEnforced())
	require.True(t, (&OperatorConfigSecurityFIPS{Enforced: types.NewStringBool(true)}).IsEnforced())
}

// TestSecurity_GetFIPS_NilSafe verifies the parent accessor handles nil at the
// container-struct level too — important because OperatorConfigSecurity
// is value-typed in OperatorConfigClickHouse so the pointer-receiver method
// must tolerate (*S)(nil) callers from indirect contexts.
func TestSecurity_GetFIPS_NilSafe(t *testing.T) {
	require.Nil(t, (*OperatorConfigSecurity)(nil).GetFIPS())

	s := &OperatorConfigSecurity{}
	require.Nil(t, s.GetFIPS())

	s.FIPS = &OperatorConfigSecurityFIPS{Enforced: types.NewStringBool(true)}
	require.NotNil(t, s.GetFIPS())
	require.True(t, s.GetFIPS().IsEnforced())
}

// TestApplyFIPSStrict_NoOpWhenDisabled is the zero-regression guard. With FIPS
// unset or disabled, normalize() must not touch any per-component knob — that
// is the entire back-compat contract.
func TestApplyFIPSStrict_NoOpWhenDisabled(t *testing.T) {
	cases := []struct {
		name string
		s    OperatorConfigSecurity
	}{
		{"no FIPS struct", OperatorConfigSecurity{}},
		{"FIPS struct present but Enforced unset", OperatorConfigSecurity{FIPS: &OperatorConfigSecurityFIPS{}}},
		{"FIPS struct present and Enforced=false", OperatorConfigSecurity{FIPS: &OperatorConfigSecurityFIPS{Enforced: types.NewStringBool(false)}}},
	}
	for _, c := range cases {
		t.Run(c.name, func(t *testing.T) {
			cfg := &OperatorConfig{Security: c.s}
			cfg.applyFIPSStrict()
			require.Nil(t, cfg.Security.ClickHouse, "ClickHouse sub-struct must remain nil")
			require.Nil(t, cfg.Security.Zookeeper, "Zookeeper sub-struct must remain nil")
			require.Nil(t, cfg.Security.Kubernetes, "Kubernetes sub-struct must remain nil")
			require.Nil(t, cfg.Security.IPC, "IPC must remain nil")
		})
	}
}

// TestApplyFIPSStrict_CoerceTable verifies every per-component knob the master switch
// is supposed to tighten. Each row is one knob; tests both "unset" and
// "explicitly relaxed" starting values to prove coercion overrides user-set
// values too (one-way tightening).
func TestApplyFIPSStrict_CoerceTable(t *testing.T) {
	cfg := &OperatorConfig{
		Security: OperatorConfigSecurity{
			FIPS: &OperatorConfigSecurityFIPS{Enforced: types.NewStringBool(true)},
			// Pre-set the OPPOSITE of the strict value for every knob so we can
			// observe the coercion actually flips them.
			ClickHouse: &ClusterSecurityClickHouse{
				TLS: &ClusterSecurityClickHouseTLS{
					Verify:     types.NewString(string(TLSVerifyNone)),
					MinVersion: types.NewString(string(TLSMinVersion12)),
				},
			},
			Zookeeper: &ClusterSecurityZookeeper{
				TLS: &ClusterSecurityZookeeperTLS{
					Verify:     types.NewString(string(TLSVerifyNone)),
					MinVersion: types.NewString(string(TLSMinVersion12)),
				},
			},
			Kubernetes: &ClusterSecurityKubernetes{
				TLS: &ClusterSecurityKubernetesTLS{
					Verify:     types.NewString(string(TLSVerifyNone)),
					MinVersion: types.NewString(string(TLSMinVersion12)),
				},
			},
			IPC: &OperatorConfigSecurityIPC{Mode: types.NewString(string(IPCModePlain))},
		},
	}

	cfg.applyFIPSStrict()

	s := cfg.Security
	require.Equal(t, TLSVerifyStrict, s.ClickHouse.GetTLS().GetVerify(), "ClickHouse.TLS.Verify must coerce to Strict")
	require.Equal(t, TLSMinVersion13, s.ClickHouse.GetTLS().GetMinVersion(), "ClickHouse.TLS.MinVersion must coerce to 1.3")
	require.Equal(t, TLSVerifyStrict, s.Zookeeper.GetTLS().GetVerify(), "Zookeeper.TLS.Verify must coerce to Strict")
	require.Equal(t, TLSMinVersion13, s.Zookeeper.GetTLS().GetMinVersion(), "Zookeeper.TLS.MinVersion must coerce to 1.3")
	// Voice E BLOCKER 2 mitigation: assert positive equality with the strict
	// target, not inequality against the relaxed one. A wrong-cell rewrite
	// (Strict → None typo in applyFIPSStrict) MUST fail this assertion.
	require.Equal(t, TLSVerifyStrict, s.Kubernetes.GetTLS().GetVerify(), "Kubernetes.TLS.Verify must coerce to Strict")
	require.Equal(t, TLSMinVersion13, s.Kubernetes.GetTLS().GetMinVersion(), "Kubernetes.TLS.MinVersion must coerce to 1.3")
	require.Equal(t, IPCModeSecure, s.IPC.GetMode(), "IPC.Mode must coerce to Secure")
}

// TestApplyFIPSStrict_AllocatesMissingSubstructs covers the case where FIPS is
// enforced but the user never set any per-component sub-struct — the master
// switch must allocate them so the coerced state is observable to downstream
// code (otherwise a nil TLS sub-struct would silently keep legacy behavior).
func TestApplyFIPSStrict_AllocatesMissingSubstructs(t *testing.T) {
	cfg := &OperatorConfig{
		Security: OperatorConfigSecurity{
			FIPS: &OperatorConfigSecurityFIPS{Enforced: types.NewStringBool(true)},
		},
	}

	cfg.applyFIPSStrict()

	s := cfg.Security
	require.NotNil(t, s.ClickHouse, "ClickHouse sub-struct must be allocated")
	require.NotNil(t, s.ClickHouse.TLS, "ClickHouse.TLS leaf must be allocated")
	require.Equal(t, TLSVerifyStrict, s.ClickHouse.TLS.GetVerify())
	require.NotNil(t, s.Zookeeper)
	require.NotNil(t, s.Zookeeper.TLS)
	require.NotNil(t, s.Kubernetes)
	require.NotNil(t, s.Kubernetes.TLS, "Kubernetes.TLS leaf must be allocated")
	require.Equal(t, TLSVerifyStrict, s.Kubernetes.TLS.GetVerify())
	require.Equal(t, TLSMinVersion13, s.Kubernetes.TLS.GetMinVersion())
	require.NotNil(t, s.IPC)
	require.Equal(t, IPCModeSecure, s.IPC.GetMode())
}

// TestStatusReasonFIPSValidationFailed verifies the reason constant value (used
// as a grep target by operators and dashboards) and that ReconcileAbortWithReason
// formats the error stream as `[reason] msg`. The reason MUST appear at the
// START of the error string — the auto-recovery skip in shouldTriggerAutoRecovery
// relies on a HasPrefix match. If the format ever grows a timestamp prefix or
// similar, this assertion fires before the skip silently breaks.
func TestStatusReasonFIPSValidationFailed(t *testing.T) {
	require.Equal(t, "FIPSValidationFailed", StatusReasonFIPSValidationFailed)

	s := &Status{}
	s.ReconcileAbortWithReason(StatusReasonFIPSValidationFailed, "ZooKeeper node zk-0:2181 must have secure=true")

	require.Equal(t, StatusAborted, s.Status)
	require.NotEmpty(t, s.Errors)
	require.True(t, strings.HasPrefix(s.Errors[0], "[FIPSValidationFailed] "),
		"reason tag must be at the START of the error (auto-recovery skip prefix-matches): got %q", s.Errors[0])
	require.Contains(t, s.Errors[0], "ZooKeeper")
}
