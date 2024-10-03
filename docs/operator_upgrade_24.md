# Upgrading ClickHouse Operator from Version 0.23 to 0.24

Upgrading the ClickHouse Operator from version **0.23** to **0.24** requires special attention due to changes in Persistent Volume Claim (PVC) naming conventions and volume management. The `volumeClaimTemplate` is now **deprecated** in favor of `dataVolumeClaimTemplate` and `logVolumeClaimTemplate`. This change affects how PVCs are named and managed.

This guide provides step-by-step instructions on how to perform the upgrade, focusing on:

- Setting the PV reclaim policy to `Retain`
- Updating the `claimRef` in the Persistent Volume (PV)
- Renaming PVCs using the `rename-pvc` plugin for `kubectl` (optional, PVCs can also be recreated)

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1: Define Variables](#step-1-define-variables)
- [Step 2: Set PV Reclaim Policy to Retain](#step-2-set-pv-reclaim-policy-to-retain)
- [Step 3: Delete the StatefulSet](#step-3-delete-the-statefulset)
- [Step 4: Rename or Recreate PVCs](#step-4-rename-or-recreate-pvcs)
  - [Option A: Rename PVCs Using `rename-pvc` Plugin](#option-a-rename-pvcs-using-rename-pvc-plugin)
  - [Option B: Manually Recreate PVCs](#option-b-manually-recreate-pvcs)
- [Step 5: Upgrade the ClickHouse Operator](#step-5-upgrade-the-clickhouse-operator)
- [Step 6: Reconcile the ClickHouseInstallation](#step-6-reconcile-the-clickhouseinstallation)

---

## Prerequisites

- **Kubernetes Cluster**: Ensure you have a Kubernetes cluster running.
- **kubectl Access**: You should have `kubectl` configured to interact with your cluster.
- **Existing ClickHouse Operator 0.23 Installation**: The operator should be installed and running.
- **Backups**: It's recommended to back up your data before proceeding.

---

## Step 1: Define Variables

First, define some variables for easier command execution:

```bash
APP_NAME=test-051-chk     # ClickHouse application name
NAMESPACE=default         # Kubernetes namespace where ClickHouse is deployed
CLUSTER_NAME=single       # Name of your ClickHouse cluster
```

---

## Step 2: Set PV Reclaim Policy to Retain

By default, when a PVC is deleted, the bound PV might also get deleted or recycled. To prevent data loss, set the PV's reclaim policy to `Retain` so that the PV and its data persist even if the PVC is deleted.

**Identify the PVCs associated with your current ClickHouse installation:**

```bash
kubectl get pvc -n $NAMESPACE -l app=$APP_NAME

# Example Output:
# NAME                        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
# both-paths-test-051-chk-0   Bound    pvc-ff79f2e4-b9fc-4357-b0ca-b073368ca0f0   1Gi        RWO            standard       10m
```

**List associated PVs:**

```bash
kubectl get pvc -n $NAMESPACE -l app=$APP_NAME -o custom-columns="PV_NAME:.spec.volumeName" --no-headers

# Example Output:
# pvc-ff79f2e4-b9fc-4357-b0ca-b073368ca0f0
```

**Save the PV name to a variable:**

```bash
PV=$(kubectl get pvc -n $NAMESPACE -l app=$APP_NAME -o jsonpath="{.items[0].spec.volumeName}")
```

**Set the PV reclaim policy to `Retain`:**

```bash
kubectl patch pv $PV -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
```

**Verify the reclaim policy:**

```bash
kubectl get pv $PV -o custom-columns="RECLAIM_POLICY:.spec.persistentVolumeReclaimPolicy" --no-headers

# Expected Output:
# Retain
```

Repeat this process for each PV associated with your ClickHouse installation.

---

## Step 3: Delete the StatefulSet

Delete the StatefulSet to detach the PVCs:

```bash
kubectl delete sts $APP_NAME -n $NAMESPACE
```

---

## Step 4: Rename or Recreate PVCs

You have two options to align your PVCs with the new naming conventions:

### Option A: Rename PVCs Using `rename-pvc` Plugin

**Install `rename-pvc` Plugin (if not already installed):**

```bash
kubectl krew update
kubectl krew install rename-pvc
```

**Identify the old PVC name:**

```bash
OLD_PVC_NAME=$(kubectl get pvc -n $NAMESPACE -l app=$APP_NAME -o jsonpath="{.items[0].metadata.name}")
```

**Determine the new PVC name using the new naming convention:**

```bash
NEW_PVC_NAME="$NAMESPACE-chk-$APP_NAME-$CLUSTER_NAME-0-0-0"
```

The new naming pattern is:

```
<namespace>-chk-<chi-name>-<cluster-name>-<shard-index>-<replica-index>-<volume-index>
```

**Rename the PVC:**

```bash
kubectl rename-pvc $OLD_PVC_NAME $NEW_PVC_NAME -n $NAMESPACE
```

When prompted, type `yes` to confirm the rename.

**Verify the PVC has the correct PV bound:**

```bash
kubectl get pvc -n $NAMESPACE

# Expected Output:
# NAME                                     STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
# default-chk-test-051-chk-single-0-0-0    Bound    pvc-ff79f2e4-b9fc-4357-b0ca-b073368ca0f0   1Gi        RWO            standard       20s
```

Repeat for each PVC.

### Option B: Manually Recreate PVCs

**Delete the old PVC:**

```bash
kubectl delete pvc $OLD_PVC_NAME -n $NAMESPACE
```

**Remove the `claimRef` from the PV:**

```bash
kubectl patch pv $PV -p '{"spec":{"claimRef": null}}'
```

**Update the `claimRef` in the PV to point to the new PVC:**

```bash
kubectl patch pv $PV -p "{
  \"spec\": {
    \"claimRef\": {
      \"name\": \"$NEW_PVC_NAME\",
      \"namespace\": \"$NAMESPACE\"
    }
  }
}"
```

**Create the new PVC:**

```bash
cat <<EOF > new-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: $NEW_PVC_NAME
  namespace: $NAMESPACE
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi  # Adjust storage size as needed
  volumeName: $PV
EOF

kubectl apply -f new-pvc.yaml
```

**Verify the PVC is bound to the PV:**

```bash
kubectl get pvc -n $NAMESPACE

# Expected Output:
# NAME                                     STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
# default-chk-test-051-chk-single-0-0-0    Bound    pvc-ff79f2e4-b9fc-4357-b0ca-b073368ca0f0   1Gi        RWO            standard       20s
```

Repeat for each PVC.

---

## Step 5: Upgrade the ClickHouse Operator

**Delete the old ClickHouse Operator deployment:**

```bash
kubectl delete deploy -n kube-system clickhouse-operator
```

**Install the new ClickHouse Operator version 0.24:**

```bash
kubectl apply -f https://raw.githubusercontent.com/Altinity/clickhouse-operator/master/deploy/operator/clickhouse-operator-install-bundle.yaml
```

---

## Step 6: Reconcile the ClickHouseInstallation

Modify your ClickHouseInstallation (CHI) manifest to comply with the new operator version, replacing deprecated fields and adjusting configurations as needed.

**Updated CHI Manifest Example (`chi-test-051-chk.yaml`):**

```yaml
apiVersion: "clickhouse-keeper.altinity.com/v1"
kind: "ClickHouseKeeperInstallation"
metadata:
  name: test-051-chk
spec:
  defaults:
    templates:
      podTemplate: default
      volumeClaimTemplate: default
      serviceTemplate: backwards-compatible
  templates:
    podTemplates:
      - name: default
        metadata:
          labels:
            app: test-051-chk
        spec:
          containers:
            - name: clickhouse-keeper
              imagePullPolicy: IfNotPresent
              image: "clickhouse/clickhouse-keeper:24.3.5.46"
              volumeMounts:
                - name: default
                  mountPath: /var/lib/clickhouse-keeper/coordination
    volumeClaimTemplates:
      - name: default
        spec:
          persistentVolumeReclaimPolicy: Retain
          accessModes:
            - ReadWriteOnce
          resources:
            requests:
              storage: 1Gi
    serviceTemplates:
      - name: backwards-compatible # operator 0.24 default service name is test-051-chk
        generateName: "test-051-chk"
        spec:
          ports:
            - name: zk
              port: 2181
          type: ClusterIP
          clusterIP: None
  configuration:
    clusters:
      - name: single
    settings:
      logger/level: "debug"
      keeper_server/tcp_port: "2181"
```

**Apply the updated CHI manifest:**

```bash
kubectl apply -f chi-test-051-chk.yaml
```

---
