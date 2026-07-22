# Rating Lab for Android

Native Kotlin/Jetpack Compose companion to the Rating Lab website. The app reads the same versioned public JSON published by GitHub Pages; it never contains source credentials or a separate rating implementation.

## First milestone

- Persistent sport switcher and bottom navigation, so primary controls never require a long return scroll.
- Compact two-line ranking cards with expandable evidence.
- Elo, Glicko-2, TrueSkill and robust-model switching from a persistent filter action.
- Native A-vs-B probability interaction with explicit surface, venue or chess-colour context.
- Compact competition forecast, player-data boundary and collapsible methodology screens.
- Online refresh with a small bundled real-world fallback for offline/error states.

## Run

Open the `android` directory in Android Studio, select an API 35 emulator or device, and run the `app` configuration.

From a terminal using Android Studio's bundled Java:

```sh
export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
./gradlew :app:assembleDebug
```

The debug APK is generated at `app/build/outputs/apk/debug/app-debug.apk`.

## Data contract

The repository reads:

```text
https://kieranmcshane.github.io/assets/data/rating-lab/{sport}.json
```

This keeps the website and Android app on one audited data pipeline. Tournament brackets and market comparison are explicitly marked as the next native integration milestone rather than represented by illustrative market data.
