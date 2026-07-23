# Rating Lab for Android

Native Kotlin/Jetpack Compose companion to the Rating Lab website. The app reads the same versioned public JSON published by GitHub Pages; it never contains source credentials or a separate rating implementation.

## Website parity

- Rankings for tennis, clubs, national teams and chess, including search, provisional gating, expandable histories and source evidence.
- Elo, Glicko-2, Gaussian TrueSkill and robust TrueSkill, with a persistent protocol action that never requires a return scroll.
- A-vs-B win/draw/loss probabilities with the website's published parameters and explicit tennis surface, football venue and chess colour controls.
- Live and upcoming competition simulations, finished-competition performance ratings, and independent Polymarket and Kalshi comparisons when the public snapshot contains them.
- The complete Historical Player Lab: men's and women's competition/season cohorts, Lineup TrueSkill, RAPM, pairwise chemistry, HAPM and LAPM, interactive comparison plot, team-scoped combinations and validation diagnostics.
- The full reproducibility surface: schema, source, freshness, licences, eligibility, parameters, evaluation metrics and direct public-data/source links.
- Compact native cards instead of horizontally scrolling web tables. Sport, section and protocol controls remain available at the screen edge on long views.
- Online refresh with a clearly marked bundled fallback for rating leaderboards when the public endpoint is unavailable. Player rankings are never fabricated offline.

## Run

Open the `android` directory in Android Studio, select an API 35 emulator or device, and run the `app` configuration.

From a terminal using Android Studio's bundled Java:

```sh
export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
export ANDROID_HOME="$HOME/Library/Android/sdk"
./gradlew :app:testDebugUnitTest :app:lintDebug :app:assembleDebug
```

The debug APK is generated at `app/build/outputs/apk/debug/app-debug.apk`.

## Data contract

The app reads:

```text
https://kieranmcshane.github.io/assets/data/rating-lab/{sport}.json
https://kieranmcshane.github.io/assets/data/rating-lab/player-football.json
```

This keeps the website and Android app on one audited pipeline. Forecasts, market quotes and player impact are displayed only when present in those versioned public payloads; the app does not invent illustrative rows.

## Release boundary

The checked-in app is production-feature complete at version 1.0.0. The repository produces a public installable debug APK for review. A Play Store release still requires the owner's Play Console account, release signing key, store listing and policy declarations; no signing credential is stored in this repository.
