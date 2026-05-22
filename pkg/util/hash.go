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
	"bytes"
	// #nosec G505 — non-security deterministic ID hashing; see HashIntoString
	// doc-comment. The operator's FIPS scope specification (§3) explicitly
	// excludes this site from the FIPS cryptographic boundary.
	"crypto/sha1"
	"encoding/gob"
	"encoding/hex"
	"fmt"
	"hash/fnv"

	dumper "github.com/sanity-io/litter"
)

func serializeUnrepeatable(obj interface{}) []byte {
	b := bytes.Buffer{}
	encoder := gob.NewEncoder(&b)
	err := encoder.Encode(obj)
	if err != nil {
		fmt.Println(`failed gob Encode`, err)
	}

	return b.Bytes()
}

func serializeRepeatable(obj interface{}) []byte {
	d := dumper.Options{
		Separator: " ",
	}
	return []byte(d.Sdump(obj))
}

// HashIntoString returns a deterministic 40-char hex digest used as a
// non-cryptographic object fingerprint / K8s label value (see Fingerprint and
// labeler.MakeObjectVersion). NOT a security control: the digest is only used
// to compare two serialized object representations for equality. Documented as
// outside the FIPS cryptographic boundary per the operator's FIPS scope (no
// integrity, signing, or authentication use). The Go runtime's `fips140=on`
// (default for GOFIPS140-built binaries) permits SHA-1 in non-approved paths;
// `fips140=only` (opt-in strict mode) would forbid it — operators running the
// optional strict-mode image variant must take that into account.
func HashIntoString(b []byte) string {
	if len(b) == 0 {
		return ""
	}
	// #nosec G401 — non-security deterministic ID hashing.
	hasher := sha1.New()
	hasher.Write(b)
	return hex.EncodeToString(hasher.Sum(nil))
}

// HashIntoInt hashes bytes and returns int version of the hash
func HashIntoInt(b []byte) int {
	if len(b) == 0 {
		return 0
	}
	h := fnv.New32a()
	_, _ = h.Write(b)
	return int(h.Sum32())
}

// HashIntoIntTopped hashes bytes and return int version of the ash topped with top
func HashIntoIntTopped(b []byte, top int) int {
	return HashIntoInt(b) % top
}
