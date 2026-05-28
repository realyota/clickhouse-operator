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

package statefulset

import (
	"context"
	"errors"
	"testing"

	"github.com/stretchr/testify/require"
	apps "k8s.io/api/apps/v1"
	apiErrors "k8s.io/apimachinery/pkg/api/errors"
	meta "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime/schema"

	api "github.com/altinity/clickhouse-operator/pkg/apis/clickhouse.altinity.com/v1"
	"github.com/altinity/clickhouse-operator/pkg/controller/common"
	"github.com/altinity/clickhouse-operator/pkg/interfaces"
)

type fakeSTS struct {
	cur       *apps.StatefulSet
	createErr error
	deleteErr error
}

func (s *fakeSTS) Get(context.Context, ...any) (*apps.StatefulSet, error) {
	return s.cur, nil
}

func (s *fakeSTS) Create(context.Context, *apps.StatefulSet) (*apps.StatefulSet, error) {
	return nil, s.createErr
}

func (s *fakeSTS) Update(context.Context, *apps.StatefulSet) (*apps.StatefulSet, error) {
	return s.cur, nil
}

func (s *fakeSTS) Delete(context.Context, string, string) error {
	return s.deleteErr
}

func (s *fakeSTS) List(context.Context, string, meta.ListOptions) ([]apps.StatefulSet, error) {
	return nil, nil
}

type testNamer struct{}

func (testNamer) Names(interfaces.NameType, ...any) []string {
	return nil
}

func (testNamer) Name(interfaces.NameType, ...any) string {
	return "chi-test-cluster-0-0"
}

type noopHostObjectsPoller struct{}

func (noopHostObjectsPoller) WaitHostStatefulSetReady(context.Context, *api.Host) error {
	return nil
}

func (noopHostObjectsPoller) WaitHostPodStarted(context.Context, *api.Host) error {
	return nil
}

func testHostWithDesiredSTS() *api.Host {
	host := &api.Host{}
	host.Runtime.SetCR(&api.ClickHouseInstallation{
		ObjectMeta: meta.ObjectMeta{
			Namespace: "default",
			Name:      "test",
		},
	})
	host.Runtime.Address.Namespace = "default"
	host.Runtime.DesiredStatefulSet = &apps.StatefulSet{
		ObjectMeta: meta.ObjectMeta{
			Namespace: "default",
			Name:      "chi-test-cluster-0-0",
		},
	}
	return host
}

func TestDoCreateStatefulSetCreateErrorAborts(t *testing.T) {
	err := apiErrors.NewAlreadyExists(
		schema.GroupResource{Group: "apps", Resource: "statefulsets"},
		"chi-test-cluster-0-0",
	)
	reconciler := &Reconciler{
		sts: &fakeSTS{createErr: err},
	}

	action := reconciler.doCreateStatefulSet(context.Background(), testHostWithDesiredSTS(), nil)

	require.ErrorIs(t, action, common.ErrCRUDAbort)
}

func TestShouldAbortOrContinueCreateStatefulSetRecreateActionAborts(t *testing.T) {
	reconciler := &Reconciler{}

	err := reconciler.shouldAbortOrContinueCreateStatefulSet(common.ErrCRUDRecreate, testHostWithDesiredSTS())

	require.ErrorIs(t, err, common.ErrCRUDAbort)
}

func TestRecreateStatefulSetDeleteErrorAborts(t *testing.T) {
	replicas := int32(1)
	errDelete := errors.New("delete timed out")
	reconciler := &Reconciler{
		hostObjectsPoller: noopHostObjectsPoller{},
		namer:             testNamer{},
		sts: &fakeSTS{
			cur: &apps.StatefulSet{
				ObjectMeta: meta.ObjectMeta{
					Namespace: "default",
					Name:      "chi-test-cluster-0-0",
				},
				Spec: apps.StatefulSetSpec{
					Replicas: &replicas,
				},
			},
			deleteErr: errDelete,
		},
	}

	err := reconciler.recreateStatefulSet(context.Background(), testHostWithDesiredSTS(), true, nil)

	require.ErrorIs(t, err, common.ErrCRUDAbort)
}
