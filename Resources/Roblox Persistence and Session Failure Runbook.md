---
title: Roblox Persistence and Session Failure Runbook
date: 2026-10-03
updated: 2026-10-03
verified: 2026-10-03
review_after: 2027-01-01
tags: [roblox, engineering, persistence, profilestore, migrations]
source: ProfileStore documentation, Roblox documentation, and local source inspection
project: null
status: actionable-not-runtime-tested
---
# Roblox Persistence and Session Failure Runbook

Related: [[Roblox Purchase Receipt Handling]], [[Fish a Monster Saving and Offline Income]], [[Roblox Vault Coverage and Maintenance]], [[Roblox Development Playbook]].

## Scope

Reusable failure-handling guidance for server-owned persistent profiles. Documentation and local source were inspected; no outage, multi-server, migration or recovery tests were executed. Proposed changes need the project's normal plan/file-list approval.

## Verified contracts

ProfileStore's API documents exclusive profile sessions, cancellation during loading, active-session checks and an end-of-session signal. A supplied Cancel callback disables its default start timeout. Steal bypasses the normal lock handoff and is explicitly unsuitable for normal player loading. LastSavedData describes a successfully persisted snapshot. Changes after session end are not persisted. Mock is in-memory storage and is not proof that real persistence works. [S1]

The tutorial releases a session if the player leaves during loading and removes access when the session ends. [S2]

Roblox data stores span places within an experience. Network calls can fail. UpdateAsync callbacks cannot yield; returning nil cancels a write. Studio can access production stores when API access is enabled; Roblox recommends a separate test experience. A Studio-specific name is useful but does not replace verifying every save path and environment. [S3]

## Recommended lifecycle and failure decisions

These are engineering recommendations, not an assertion that all project callers already comply.

| State or event | Required behaviour | Failure to prevent |
|---|---|---|
| Loading | Gate reward, purchase grant, trade and inventory mutation; supply cancellation for leave/shutdown and an explicit chosen deadline | Infinite loading or playing on unsaved defaults |
| Load returns no profile | Explain the failure and end the attempt; preserve the existing key | Mistaking unavailable data for a new player |
| Loaded | Attach session-loss handling; validate schema and data before exposing a usable profile | Other systems seeing partially migrated state |
| Active mutation | Check ownership immediately before a non-yielding mutation; reacquire state after asynchronous work | Continuing with a stale table/session |
| Session ends | Remove public access, cancel player jobs and pending mutations; transition the player out of authoritative play | Old server granting after another server owns the profile |
| Player leaves while load finishes | Release the newly acquired session without starting gameplay | Orphaned locks and unnecessary work |
| Save requested | Distinguish request, confirmed persistence and failure; use saved-state evidence for paid rewards | Claiming a write succeeded because Save returned |
| Shutdown | Let the library release owned sessions; avoid introducing a second competing save writer | Last-writer corruption and duplicate teardown |
| Prolonged store degradation | Surface service status, observe failures and limit risky new commitments using a defined policy | Repeated unsupported promises that progress is safe |

A session lock is not a transaction across two players or two keys. Trading/gifting needs a separate recoverable protocol before implementation. Do not bypass a lock to make an outage disappear.

## Migration and repair procedure

1. Identify source and target schema. Reject a newer schema without coercing it backwards.
2. Work on a deep candidate copy. Apply ordered migration steps; validate shapes, finite numbers, ranges, references and uniqueness.
3. Run repair and dependent derived-state setup inside the same controlled failure boundary. Only expose or commit the candidate after success.
4. Treat lost valuable items as a support/recovery question, not an automatic reason to drop unknown IDs. Distinguish retired content from a bad catalog deployment.
5. Record migration outcome and version. Re-running an already-current migration must not repeat rewards or resets.
6. Test downgrade/rollback compatibility before release: rolling code back does not roll stored data back.
7. On unexpected failure, stop gameplay, release the session and retain diagnostic identifiers. Do not replace the key with defaults.

For a suspected bad migration, first stop the affected writer or feature, identify affected versions/cohorts, and preserve evidence. Rehearse restoration on a test copy. Determine whether restoring old state would remove legitimate later purchases or progress; recovery requires reconciliation, not a blind bulk overwrite.

## Local inspection: Paper Plane Toss

Read on 2026-10-03 from C:\Users\holde\Downloads\SecondGame:

- wally.lock pins lm-loleris/profilestore 1.0.3. Its installed Save and EndSession methods spawn save work; they are not synchronous persistence acknowledgements.
- Config uses schema 8, Studio store PPT_Players_Studio_v1 and live store PPT_Players_v1.
- PlayerData.update checks IsActive before invoking the mutation, but does not enforce non-yielding callbacks or roll back ordinary callback errors. Callers need an explicit contract. PlayerData.get returns the actual mutable table despite its read-only comment.
- The load Cancel callback checks player departure only. Installed library code checks its default 120-second timeout only when Cancel is absent. **Finding:** this integration lacks an explicit elapsed-time deadline in its custom cancellation path. This does not mean a request always hangs; the risk is prolonged loading during repeated failures while the player remains present.
- Migration runs on a deep copy under pcall and rejects future schemas. The candidate is copied into the real profile before Reconcile, repair and resumePotions. Those later calls are outside that migration pcall, and the session-end listener is attached afterwards. **Review gap:** an unexpected error there can interrupt cleanup/setup after the migration is committed in memory. No reproduced incident is claimed.
- Receipt processing has a different copy-and-commit path; see [[Roblox Purchase Receipt Handling]]. Do not generalise its protection to ordinary update calls.

Source fingerprints (SHA256): PlayerData.luau = 3BED3316D2A9A2410F0E5ADE210FE26B54D3335F5905690267DD39575CF73A79; ProfileSanitize.luau = 6CD818721ACD61DB764C07F2944946FC04CF119D1C5376BCCBF321B5CF07C22C; installed ProfileStore.luau = 799263DC0D281F360432E172F57EF337761EC38482575273B3CB079D114ECF71. These identify inspected files, not a deployed build.

## Acceptance matrix to execute before claiming readiness

| Scenario | Expected evidence |
|---|---|
| Existing key temporarily unreadable | No default overwrite; failed load is visible |
| Player leaves mid-load | No gameplay registration; acquired session released |
| Repeated load failures while player stays | Explicit deadline ends loading; no forced steal |
| Same account enters another server | Ownership handoff; prior server mutations stop |
| Mutation attempts after session end | Rejected; no reward UI implying success |
| Ordinary mutation errors halfway | Defined rollback/validation behaviour demonstrated, not assumed from pcall |
| Save request fails, then succeeds | Separate request/failure/confirmation records |
| Old, current and future schema fixtures | Expected transformations; current rerun unchanged; future rejected |
| Repair or setup throws | Session cleanup occurs and no partial gameplay exposure |
| Restart in separate test experience | Persisted values survive; not merely Mock memory |
| Recovery rehearsal | Restored candidate validated; subsequent paid progress reconciled |

Record library version, build identity, test key/environment, injected failure, expected/actual result and remaining risk. Avoid logging complete player profiles or secrets. Useful observability: load duration/outcome, migration failures by version, session-loss count, save errors and last confirmed persistence time.

## Sources

Checked 2026-10-03:
- [S1: ProfileStore API](https://madstudioroblox.github.io/ProfileStore/api/)
- [S2: ProfileStore tutorial](https://madstudioroblox.github.io/ProfileStore/tutorial/)
- [S3: Roblox data stores](https://create.roblox.com/docs/cloud-services/data-stores)
- Local: C:\Users\holde\Downloads\SecondGame\wally.lock
- Local: C:\Users\holde\Downloads\SecondGame\src\shared\Config.luau
- Local: C:\Users\holde\Downloads\SecondGame\src\server\Systems\PlayerData.luau
- Local: C:\Users\holde\Downloads\SecondGame\src\server\Lib\ProfileSanitize.luau
- Local: C:\Users\holde\Downloads\SecondGame\ServerPackages\_Index\lm-loleris_profilestore@1.0.3\profilestore\ProfileStore.luau
