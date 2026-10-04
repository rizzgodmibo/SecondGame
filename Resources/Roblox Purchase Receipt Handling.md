---
title: Roblox Purchase Receipt Handling
date: 2026-10-03
tags: [roblox, monetization, profilestore, security]
updated: 2026-10-03
verified: 2026-10-03
review_after: 2026-11-02
status: sourced-not-retested
---
# Roblox Purchase Receipt Handling

Historical lessons from the Phase 10a audit of [[Paper Plane Toss Monetization]], with a source review on 2026-10-03. This review does not retest the project implementation. The ProfileStore cached-receipt example is a reference pattern with limitations, not proof of exactly-once delivery forever.

- **Confirm durable reward and receipt state before acknowledging a persistent grant.** ProfileStore's cached-ID example checks LastSavedData before returning PurchaseGranted. The earlier 50-ID cap was project guidance; the current library example uses 100. Neither finite cache proves permanent duplicate prevention: an evicted ID can no longer be recognised by that cache. Review retention and delayed retries before reuse.
- **Account for a receipt arriving before profile load.** The ProfileStore example waits while the player remains present, then checks profile availability. A 45-second timeout is a project choice, not an engine contract. NotProcessedYet defers acknowledgement; do not describe it as permanent loss or assume an immediate retry. Confirm retry behaviour against current API documentation before implementation.
- **Run each grant on a copy** of the profile and commit only if it finishes without error. Otherwise a grant that fails halfway keeps partial rewards, and Roblox's retry adds them again.
- Project implementation recommendation: keep the in-memory reward mutation non-yielding. The outer receipt handler may wait for loading or persistence; do not confuse the two.
- If a manual save fails, retry about every 10 s instead of polling every frame until the next autosave.
- **Don't send receipt ids to the client** on every profile update. It wastes bandwidth.
- **Pass entitlement history, not a verified refund protocol:** the project sought to remove effects when ownership was lost and avoid stale checks revoking a same-session purchase. Current ownership caching, refund signals and revocation behaviour still need source verification. A failed lookup alone is not evidence that ownership was lost.
- Type-check receipt fields before using them.
- Wrap per-player server loops (Auto Throw) in `pcall`, so one player's error doesn't stop the loop for everyone.

Related: [[Fish a Monster Saving and Offline Income]]

## Reuse conditions and failure tests

Engineering recommendations from this review:
- Persist the reward and duplicate marker together in the authoritative profile mutation. A separate receipt ledger plus a separate balance write introduces a crash window unless a recovery protocol handles it.
- A pcall does not undo mutations. The historical copy-and-commit approach must include nested mutable data; a shallow copy can still leak partial changes. Keep external side effects out of the transaction.
- Serialise overlapping processing for a purchase/player and honour session ownership. On session loss, stop mutating the profile.
- Calling Save is not itself proof of persistence. Use the library's documented saved-state evidence.
- Do not silently acknowledge an unknown product. Preserve its pending state and investigate the mapping.

Acceptance scenarios to execute before reuse: duplicate delivery before/after save; crash before save; crash after save but before acknowledgement; two receipts overlapping; profile load failure; session loss during save; grant error after partial mutation; unknown product; replay of an ID evicted from the cache. Record expected reward count and persisted state for each. No tests were run in this documentation pass.

## Open API/version questions

The current MarketplaceService reference also lists BindReceiptHandler. Its contract and deployment availability were not audited here. Do not mix its ReceiptDecision enum with ProcessReceipt's ProductPurchaseDecision or migrate the project solely from an example. Pin the project's ProfileStore version and inspect it before adapting the library's current example.

Related: [[Roblox Development Playbook]], [[Roblox Vault Coverage and Maintenance]].

## Sources

Checked 2026-10-03:
- [ProfileStore developer products](https://madstudioroblox.github.io/ProfileStore/devproducts/) — profile-load wait, cached IDs, saved-state confirmation and example cache size.
- [MarketplaceService API reference](https://create.roblox.com/docs/reference/engine/classes/MarketplaceService) — callback and handler API surface; full retry semantics remain an explicit verification gap.
- Local historical source: [[Paper Plane Toss Monetization]]. Recommendations above are engineering analysis, not newly executed project tests.
