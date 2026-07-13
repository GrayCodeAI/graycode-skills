---
name: minimax-android-native-dev
description: Android native application development and UI design guide. Covers Material
  Design 3, Kotlin/Compose development, project configuration, accessibility, and
  build troubleshooting. Read this before A...
license: MIT
tags:
- mobile
metadata: None
version: 1.0.0
category: mobile
sources: None
---

## 8. Testing

> **Note**: Only add test dependencies when the user explicitly asks for testing.

A well-tested Android app uses layered testing: fast local unit tests for logic, instrumentation tests for UI and integration, and Gradle Managed Devices to run emulators reproducibly on any machine — including CI.

### 8.1 Test Dependencies

Before adding test dependencies, inspect the project's existing versions to avoid conflicts:

1. Check `gradle/libs.versions.toml` — if present, add test deps using the project's version catalog style
2. Check existing `build.gradle.kts` for already-pinned dependency versions
3. Match version families using the table below

**Version Alignment Rules**:

| Test Dependency                              | Must Align With                                  | How to Check                                                          |
|----------------------------------------------|--------------------------------------------------|-----------------------------------------------------------------------|
| `kotlinx-coroutines-test`                    | Project's `kotlinx-coroutines-core` version      | Search for `kotlinx-coroutines` in build files or version catalog     |
| `compose-ui-test-junit4`                     | Project's Compose BOM or `compose-compiler`      | Search for `compose-bom` or `compose.compiler` in build files         |
| `espresso-*`                                 | All Espresso artifacts must use the same version  | Search for `espresso` in build files                                  |
| `androidx.test:runner`, `rules`, `ext:junit` | Should use compatible AndroidX Test versions      | Search for `androidx.test` in build files                             |
| `mockk`                                      | Must support the project's Kotlin version         | Check `kotlin` version in root `build.gradle.kts` or version catalog |

**Dependencies Reference** — add only the groups you need:

```kotlin
dependencies {
    // --- Local unit tests (src/test/) ---
    testImplementation("junit:junit:<version>")                          // 4.13.2+
    testImplementation("org.robolectric:robolectric:<version>")          // 4.16.1+
    testImplementation("io.mockk:mockk:<version>")                      // match Kotlin version
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:<version>")  // match coroutines-core
    testImplementation("androidx.arch.core:core-testing:<version>")      // InstantTaskExecutorRule for LiveData
    testImplementation("app.cash.turbine:turbine:<version>")             // Flow/StateFlow testing

    // --- Instrumentation tests (src/androidTest/) ---
    androidTestImplementation("androidx.test.ext:junit:<version>")
    androidTestImplementation("androidx.test:runner:<version>")
    androidTestImplementation("androidx.test:rules:<version>")
    androidTestImplementation("androidx.test.espresso:espresso-core:<version>")
    androidTestImplementation("androidx.test.espresso:espresso-contrib:<version>")   // RecyclerView, Drawer
    androidTestImplementation("androidx.test.espresso:espresso-intents:<version>")   // Intent verification
    androidTestImplementation("androidx.test.espresso:espresso-idling-resource:<version>")
    androidTestImplementation("androidx.test.uiautomator:uiautomator:<version>")

    // --- Compose UI tests (only if project uses Compose) ---
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")      // version from Compose BOM
    debugImplementation("androidx.compose.ui:ui-test-manifest")          // required for createComposeRule
}
```

> **Note**: If the project uses a Compose BOM, `ui-test-junit4` and `ui-test-manifest` don't need explicit versions — the BOM manages them.

Enable Robolectric resource support in the `android` block:

```kotlin
android {
    testOptions {
        unitTests.isIncludeAndroidResources = true  // required for Robolectric
    }
}
```

### 8.2 Testing by Layer

| Layer              | Location           | Runs On                 | Speed                | Use For                                          |
|--------------------|--------------------|-------------------------|----------------------|--------------------------------------------------|
| Unit (JUnit)       | `src/test/`        | JVM                     | ~ms                  | ViewModels, repos, mappers, validators           |
| Unit + Robolectric | `src/test/`        | JVM + simulated Android | ~100ms               | Code needing Context, resources, SharedPrefs     |
| Compose UI (local) | `src/test/`        | JVM + Robolectric       | ~100ms               | Composable rendering & interaction               |
| Espresso           | `src/androidTest/` | Device/Emulator         | ~seconds             | View-based UI flows, Intents, DB integration     |
| Compose UI (device)| `src/androidTest/` | Device/Emulator         | ~seconds             | Full Compose UI flows with real rendering        |
| UI Automator       | `src/androidTest/` | Device/Emulator         | ~seconds             | System dialogs, notifications, multi-app         |
| Managed Device     | `src/androidTest/` | Gradle-managed AVD      | ~minutes (first run) | CI, matrix testing across API levels             |

See Testing for detailed examples, code patterns, and Gradle Managed Device configuration.

### 8.3 Testing Commands

```bash
# Local unit tests (fast, no emulator)
./gradlew test                          # all modules
./gradlew :app:testDebugUnitTest        # app module, debug variant

# Single test class
./gradlew :app:testDebugUnitTest --tests "com.example.myapp.CounterViewModelTest"

# Instrumentation tests (requires device or managed device)
./gradlew connectedDebugAndroidTest     # on connected device
./gradlew pixel6Api34DebugAndroidTest   # on managed device

# Both together
./gradlew test connectedDebugAndroidTest

# Test with coverage report (JaCoCo)
./gradlew testDebugUnitTest jacocoTestReport
```
