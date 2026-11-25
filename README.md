## Verification & CI

Automated verification runs via `.github/workflows/coniunctio_ci.yml` on every
push and pull request:

* `test_coniunctio.py` across four primary test profiles:
  * Balanced tension
  * Strong symmetry
  * Reversed asymmetry
  * Zero-tension ground state
* `pytest -q`
* `preservation_seed_v2.py`: 23 tests, run unkeyed and keyed (HMAC)
* Simulation run, trajectory analysis and artifact upload

### Seal modes (`preservation_seed_v2.py`)

* **Unkeyed (default):** a plain SHA-256 digest. It detects accidental edits
  and corruption, but anyone can recompute it, so it does not authenticate
  who wrote the file.
* **Keyed:** set `SEED_HMAC_KEY` and the seal becomes HMAC-SHA256. The same
  key must be set wherever a seed is verified, inspected or stepped. Payload
  fields stay plain text on disk; the key authenticates, it does not encrypt.

Seeds sealed by 1.2 files use a different canonical encoding and will not
verify under 2.0. Re-export them.

### Seed validation (`preservation_seed_v2.py`)

Loading a seed rejects `NaN`, `Infinity` and `-Infinity` (including overflow
literals such as `1e999`), non-finite floats, and `active_friction < 0`.
Seals are compared with `hmac.compare_digest`.