# Soul Shredder

A skateboarding quest game by Oatmeal Morning. Play it at https://soulshredder.oatmealmorning.com

- `index.html`: the live game. Built from Guy's file, never edited by hand.
- `guy/soul-shredder-release.html`: Guy's release build, exactly as received.
- `tools/apply_web_edits.py`: turns Guy's build into `index.html` (head and preview tags, embedded font, analytics, share address). When Guy sends a new build: replace the file in `guy/`, then run `python3 tools/apply_web_edits.py guy/soul-shredder-release.html index.html`.
- `privacy/`, `support/`: the policy and support pages (also used by the app stores).
- `store-kit/`: store listing assets and text for Google Play and the App Store.

Browser storage keys are permanent (players' progress): `ss_best`, `ss_mute`, `ss_l1done`, `ss_l2done`, `ss_l3done`; app builds also `ss_pid`. Analytics: shared PostHog project, every event has `app: 'soulshredder'`.

Font: Press Start 2P, SIL Open Font License (tools/press-start-2p-OFL.txt).

© 2026 Oatmeal Morning
