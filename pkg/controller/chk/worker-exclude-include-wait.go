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

package chk

import (
	"context"
	"time"

	log "github.com/altinity/clickhouse-operator/pkg/announcer"
	apiChk "github.com/altinity/clickhouse-operator/pkg/apis/clickhouse-keeper.altinity.com/v1"
	"github.com/altinity/clickhouse-operator/pkg/util"
)

func (w *worker) waitForIPAddresses(ctx context.Context, chk *apiChk.ClickHouseKeeperInstallation) {
	if util.IsContextDone(ctx) {
		log.V(2).Info("task is done")
		return
	}
	if chk.IsStopped() {
		// No need to wait for stopped CHI
		return
	}
	w.a.V(1).M(chk).F().S().Info("wait for IP addresses to be assigned to all pods")
	start := time.Now()
	w.c.poll(ctx, chk, func(c *apiChk.ClickHouseKeeperInstallation, e error) bool {
		// TODO fix later
		// status IPs list can be empty
		// Instead of doing in status:
		// 	podIPs := c.getPodsIPs(chi)
		//	cur.EnsureStatus().SetPodIPs(podIPs)
		// and here
		// c.Status.GetPodIPs()
		podIPs := w.c.getPodsIPs(chk)
		if len(podIPs) >= len(c.Status.GetPods()) {
			// Stop polling
			w.a.V(1).M(c).Info("all IP addresses are in place")
			return false
		}
		if time.Now().Sub(start) > 1*time.Minute {
			// Stop polling
			w.a.V(1).M(c).Warning("not all IP addresses are in place but time has elapsed")
			return false
		}
		// Continue polling
		w.a.V(1).M(c).Warning("still waiting - not all IP addresses are in place yet")
		return true
	})
}
