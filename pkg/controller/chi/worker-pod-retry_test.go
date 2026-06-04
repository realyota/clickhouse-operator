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

package chi

import (
	"strconv"
	"testing"
	"time"

	"github.com/stretchr/testify/require"
	core "k8s.io/api/core/v1"
	meta "k8s.io/apimachinery/pkg/apis/meta/v1"

	api "github.com/altinity/clickhouse-operator/pkg/apis/clickhouse.altinity.com/v1"
)

// pod is a small builder for a Pod with one container and the given readiness flag.
func pod(ready bool) *core.Pod {
	return &core.Pod{
		Status: core.PodStatus{
			ContainerStatuses: []core.ContainerStatus{
				{Name: "clickhouse", Ready: ready},
			},
		},
	}
}

// multiContainerPod is a builder for a Pod with multiple containers, each with
// individually controllable readiness. The pod is "ready" only if all containers are.
// Container names use strconv.Itoa so an arbitrary number of containers is supported.
func multiContainerPod(readiness ...bool) *core.Pod {
	p := &core.Pod{Status: core.PodStatus{}}
	for i, r := range readiness {
		p.Status.ContainerStatuses = append(p.Status.ContainerStatuses, core.ContainerStatus{
			Name:  "c" + strconv.Itoa(i),
			Ready: r,
		})
	}
	return p
}

// TestIsPodNotReadyToReadyTransition verifies the pure transition-detection logic
// used by recoverAbortedReconcileOnPodReady.
func TestIsPodNotReadyToReadyTransition(t *testing.T) {
	tests := []struct {
		name     string
		old, new *core.Pod
		expected bool
	}{
		{"nil old", nil, pod(true), false},
		{"nil new", pod(false), nil, false},
		{"both nil", nil, nil, false},
		{"not ready → ready (the target case)", pod(false), pod(true), true},
		{"ready → ready (no transition)", pod(true), pod(true), false},
		{"ready → not ready (wrong direction)", pod(true), pod(false), false},
		{"not ready → not ready", pod(false), pod(false), false},
		{"multi-container: one not ready → all ready", multiContainerPod(true, false), multiContainerPod(true, true), true},
		{"multi-container: all ready → one not ready", multiContainerPod(true, true), multiContainerPod(false, true), false},
		{"multi-container: all ready → all ready", multiContainerPod(true, true), multiContainerPod(true, true), false},
		// Edge case: PodHasNotReadyContainers returns false for an empty ContainerStatuses
		// slice (zero-length loop). So a pod with no statuses yet is effectively treated as
		// "ready". When the first pod event we see already has ready statuses, the transition
		// does NOT fire — we only react to observed NotReady→Ready flips, not to pods that
		// were already ready when we started observing them.
		{"empty container statuses → ready (startup edge, no transition)", &core.Pod{}, pod(true), false},
		// Many containers — exercises strconv-based naming in the builder.
		{"12-container pod: last flips to ready",
			multiContainerPod(true, true, true, true, true, true, true, true, true, true, true, false),
			multiContainerPod(true, true, true, true, true, true, true, true, true, true, true, true),
			true},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			got := isPodNotReadyToReadyTransition(tc.old, tc.new)
			require.Equal(t, tc.expected, got)
		})
	}
}

// TestShouldTriggerAutoRecovery verifies the CR-state gate used by
// recoverAbortedReconcileOnPodReady.
func TestShouldTriggerAutoRecovery(t *testing.T) {
	// Minimal CHI builder. The Status struct has no setter — field is set directly.
	makeCR := func(status string, deleting bool) *api.ClickHouseInstallation {
		cr := &api.ClickHouseInstallation{
			ObjectMeta: meta.ObjectMeta{Name: "chi", Namespace: "ns"},
		}
		cr.EnsureStatus().Status = status
		if deleting {
			now := meta.NewTime(time.Now())
			cr.ObjectMeta.DeletionTimestamp = &now
		}
		return cr
	}

	// withError builds an Aborted CR carrying a reason-tagged latest error.
	withError := func(reason, msg string) *api.ClickHouseInstallation {
		cr := makeCR(api.StatusAborted, false)
		cr.EnsureStatus().Errors = []string{"[" + reason + "] " + msg}
		return cr
	}

	tests := []struct {
		name     string
		cr       *api.ClickHouseInstallation
		expected bool
	}{
		{"nil CR — reject", nil, false},
		{"Aborted, not deleting — accept (the target case)", makeCR(api.StatusAborted, false), true},
		{"Completed — reject (nothing to recover)", makeCR(api.StatusCompleted, false), false},
		{"InProgress — reject (reconcile already running)", makeCR(api.StatusInProgress, false), false},
		{"Terminating — reject", makeCR(api.StatusTerminating, false), false},
		{"Aborted but being deleted — reject", makeCR(api.StatusAborted, true), false},
		{"empty status (fresh CR) — reject", makeCR("", false), false},
		// Normalize-time abort reasons: pod-Ready flips can't recover these.
		{"Aborted with FIPSValidationFailed — reject (spec edit required)",
			withError(api.StatusReasonFIPSValidationFailed, "ZK plain-text rejected"), false},
		{"Aborted with RootCAConflict — reject",
			withError(api.StatusReasonRootCAConflict, "rootCA and rootCASecretRef both set"), false},
		{"Aborted with RootCASecretUnresolved — reject",
			withError(api.StatusReasonRootCASecretUnresolved, "secret/key not found"), false},
		{"Aborted with FIPSImagePolicyViolation — reject",
			withError(api.StatusReasonFIPSImagePolicyViolation, "image lacks fips marker"), false},
		// Generic Aborted with an unrecognized reason tag — still a recovery target.
		{"Aborted with unrecognized reason — accept",
			withError("SomeOtherReason", "generic abort"), true},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			require.Equal(t, tc.expected, shouldTriggerAutoRecovery(tc.cr))
		})
	}
}
