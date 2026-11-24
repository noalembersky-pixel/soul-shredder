# Soul Shredder

A skateboarding quest game by Oatmeal Morning, for iPhone and Android.
Website (store page only): https://soulshredder.oatmealmorning.com

**Decided 24 Nov 2026: the website never has the playable game.** The game only ships inside the apps.

- `docs/`: the website, and the only folder GitHub Pages publishes (Settings → Pages → Branch `main` / `/docs`).
  - `index.html`: home page = a copy of `get/` (store badges or "Coming soon"), canonical = the root address, PostHog `page: 'home'`.
  - `get/`: store landing page the apps share (PostHog `page: 'get'`). Keep the address; the apps link to it.
  - `privacy/`, `support/`: policy and support pages (also used by the app stores).
  - `CNAME`: the web address. Never remove it.
- `guy/soul-shredder-release.html`: Guy's release build, exactly as received. Not published.
- `tools/apply_web_edits.py`: turns Guy's build into the app game file. It only makes app builds and refuses to write into `docs/` or the repo root:
  - Android: `python3 tools/apply_web_edits.py guy/soul-shredder-release.html /tmp/ss-android/index.html --platform android --version 1.0` → copy to `soulshredder-app/app-web/index.html`.
  - iOS: same with `--platform ios` → copy to `soulshredder-ios/www/index.html` AND `soulshredder-ios/ios/App/App/public/index.html`.
  - When Guy sends a new build: replace the file in `guy/`, rerun both commands, rebuild the apps.
- `store-kit/`: store listing assets and text. Not published.

Never put a game file (Guy's build or a script output) inside `docs/`.

Browser storage keys are permanent (players' progress): `ss_best`, `ss_mute`, `ss_l1done`, `ss_l2done`, `ss_l3done`; app builds also `ss_pid`. Analytics: shared PostHog project, every event has `app: 'soulshredder'`.

Font: Press Start 2P, SIL Open Font License (tools/press-start-2p-OFL.txt).

© 2026 Oatmeal Morning
