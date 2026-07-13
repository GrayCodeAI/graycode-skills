Sometimes you may find yourself with a large list of work to be processed.

While it is possible to just enqueue "all" those work items to a task group like this:

```swift
// Potentially wasteful -- perhaps this creates thousands of tasks concurrently (?!)

let lotsOfWork: [Work] = ...
await withTaskGroup(of: Something.self) { group in
  for work in lotsOfWork {
    // If this is thousands of items, we may end up creating a lot of tasks here.
    group.addTask {
      await work.work()
    }
  }

  for await result in group {
    process(result) // process the result somehow, depends on your needs
  }
}
```

If you expect to deal with hundreds or thousands of items, it might be inefficient to enqueue them all immediately.
Creating a task (in `addTask`) allocates memory for the task in order to suspend and execute it.
While the amount of memory for each task isn't large, it can be significant when creating thousands of tasks that won't execute immediately.

When faced with such a situation, you can manually throttle the number of concurrently added tasks in the group, as follows:

```swift
let lotsOfWork: [Work] = ... 
let maxConcurrentWorkTasks = min(lotsOfWork.count, 10)
assert(maxConcurrentWorkTasks > 0)

await withTaskGroup(of: Something.self) { group in
    var submittedWork = 0
    for _ in 0..<maxConcurrentWorkTasks {
        group.addTask { // or 'addTaskUnlessCancelled'
            await lotsOfWork[submittedWork].work() 
        }
        submittedWork += 1
    }
    
    for await result in group {
        process(result) // process the result somehow, depends on your needs
    
        // Every time we get a result back, check if there's more work we should submit and do so
        if submittedWork < lotsOfWork.count, 
           let remainingWorkItem = lotsOfWork[submittedWork] {
            group.addTask { // or 'addTaskUnlessCancelled'
                await remainingWorkItem.work() 
            }  
            submittedWork += 1
        }
    }
}
```



================================================
FILE: Guide.docc/SourceCompatibility.md
================================================
# Source Compatibility

See an overview of potential source compatibility issues.

Swift 6 includes a number of evolution proposals that could potentially affect
source compatibility.
These are all opt-in for the Swift 5 language mode.

> Note: For the previous release’s Migration Guide, see [Migrating to Swift 5][swift5].

[swift5]: https://www.swift.org/migration-guide-swift5/

## Handling Future Enum Cases

[SE-0192][]: `NonfrozenEnumExhaustivity`

Lack of a required `@unknown default` has changed from a warning to an error.

[SE-0192]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0192-non-exhaustive-enums.md

## Concise magic file names

[SE-0274][]: `ConciseMagicFile`

The special expression `#file` has changed to a human-readable string
containing the filename and module name.

[SE-0274]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0274-magic-file.md

## Forward-scan matching for trailing closures

[SE-0286][]: `ForwardTrailingClosures`

Could affect code involving multiple, defaulted closure parameters.

[SE-0286]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0286-forward-scan-trailing-closures.md

## Incremental migration to concurrency checking

[SE-0337][]: `StrictConcurrency`

Will introduce errors for any code that risks data races.

[SE-0337]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0337-support-incremental-migration-to-concurrency-checking.md

> Note: This feature implicitly also enables [`IsolatedDefaultValues`](#Isolated-default-value-expressions),
[`GlobalConcurrency`](#Strict-concurrency-for-global-variables),
and [`RegionBasedIsolation`](#Region-based-Isolation).

## Implicitly Opened Existentials

[SE-0352][]: `ImplicitOpenExistentials`

Could affect overload resolution for functions that involve both
existentials and generic types.

[SE-0352]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0352-implicit-open-existentials.md

## Regex Literals

[SE-0354][]: `BareSlashRegexLiterals`

Could impact the parsing of code that was previously using a bare slash.

[SE-0354]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0354-regex-literals.md

## Deprecate @UIApplicationMain and @NSApplicationMain

[SE-0383][]: `DeprecateApplicationMain`

Will introduce an error for any code that has not migrated to using `@main`.

[SE-0383]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0383-deprecate-uiapplicationmain-and-nsapplicationmain.md

## Importing Forward Declared Objective-C Interfaces and Protocols

[SE-0384][]: `ImportObjcForwardDeclarations`

Will expose previously-invisible types that could conflict with existing
sources.

[SE-0384]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0384-importing-forward-declared-objc-interfaces-and-protocols.md

## Remove Actor Isolation Inference caused by Property Wrappers

[SE-0401][]: `DisableOutwardActorInference`

Could change the inferred isolation of a type and its members.

[SE-0401]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0401-remove-property-wrapper-isolation.md

## Isolated default value expressions

[SE-0411][]: `IsolatedDefaultValues`

Will introduce errors for code that risks data races.

[SE-0411]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0411-isolated-default-values.md

##  Strict concurrency for global variables

[SE-0412][]: `GlobalConcurrency`

Will introduce errors for code that risks data races.

[SE-0412]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0412-strict-concurrency-for-global-variables.md

## Region based Isolation

[SE-0414][]: `RegionBasedIsolation`

Increases the constraints of the `Actor.assumeIsolated` function.

[SE-0414]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0414-region-based-isolation.md

## Inferring `Sendable` for methods and key path literals

[SE-0418][]: `InferSendableFromCaptures`

Could affect overload resolution for functions that differ only by sendability.

[SE-0418]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0418-inferring-sendable-for-methods.md

## Dynamic actor isolation enforcement from non-strict-concurrency contexts

[SE-0423][]: `DynamicActorIsolation`

Introduces new assertions that could affect existing code if the runtime
isolation does not match expectations.

[SE-0423]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0423-dynamic-actor-isolation.md

## Usability of global-actor-isolated types

[SE-0434][]: `GlobalActorIsolatedTypesUsability`

Could affect type inference and overload resolution for functions that are
globally-isolated but not `@Sendable`. 

[SE-0434]: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0434-global-actor-isolated-types-usability.md



================================================
FILE: Guide.docc/Swift6Mode.md
================================================
# Enabling The Swift 6 Language Mode

Guarantee your code is free of data races by enabling the Swift 6 language mode.

## Using the Swift compiler

To enable the Swift 6 language mode when running `swift` or `swiftc`
directly at the command line, pass `-swift-version 6`:

```
~ swift -swift-version 6 main.swift
```

## Using SwiftPM

### Command-line invocation

`-swift-version 6` can be passed in a Swift package manager command-line
invocation using the `-Xswiftc` flag:

```
~ swift build -Xswiftc -swift-version -Xswiftc 6
~ swift test -Xswiftc -swift-version -Xswiftc 6
```

### Package manifest

A `Package.swift` file that uses `swift-tools-version` of `6.0` will enable the Swift 6 language
mode for all targets. You can still set the language mode for the package as a whole using the
`swiftLanguageModes` property of `Package`. However, you can now also change the language mode as
needed on a per-target basis using the new `swiftLanguageMode` build setting:

```swift
// swift-tools-version: 6.0

let package = Package(
    name: "MyPackage",
    products: [
        // ...
    ],
    targets: [
        // Uses the default tools language mode (6)
        .target(
            name: "FullyMigrated",
        ),
        // Still requires 5
        .target(
            name: "NotQuiteReadyYet",
            swiftSettings: [
                .swiftLanguageMode(.v5)
            ]
        )
    ]
)
```

Note that if your package needs to continue supporting earlier Swift toolchain versions and you want
to use per-target `swiftLanguageMode`, you will need to create a version-specific manifest for pre-6
toolchains. For example, if you'd like to continue supporting 5.9 toolchains and up, you could have
one manifest `Package@swift-5.9.swift`:
```swift
// swift-tools-version: 5.9

let package = Package(
    name: "MyPackage",
    products: [
        // ...
    ],
    targets: [
        .target(
            name: "FullyMigrated",
        ),
        .target(
            name: "NotQuiteReadyYet",
        )
    ]
)
```

And another `Package.swift` for Swift toolchains 6.0+:
```swift
// swift-tools-version: 6.0

let package = Package(
    name: "MyPackage",
    products: [
        // ...
    ],
    targets: [
        // Uses the default tools language mode (6)
        .target(
            name: "FullyMigrated",
        ),
        // Still requires 5
        .target(
            name: "NotQuiteReadyYet",
            swiftSettings: [
                .swiftLanguageMode(.v5)
            ]
        )
    ]
)
```

If instead you would just like to use Swift 6 language mode when it's available (while still
continuing to support older modes) you can keep a single `Package.swift` and specify the version in
a compatible manner:
```swift
// swift-tools-version: 5.9

let package = Package(
    name: "MyPackage",
    products: [
        // ...
    ],
    targets: [
        .target(
            name: "FullyMigrated",
        ),
    ],
    // `swiftLanguageVersions` and `.version("6")` to support pre 6.0 swift-tools-version.
    swiftLanguageVersions: [.version("6"), .v5]
)
```


## Using Xcode

### Build Settings

You can control the language mode for an Xcode project or target by setting
the "Swift Language Version" build setting to "6".

### XCConfig

You can also set the `SWIFT_VERSION` setting to `6` in an xcconfig file:

```
// In a Settings.xcconfig

SWIFT_VERSION = 6;
```



================================================
FILE: Sources/Examples/Boundaries.swift
================================================
import Library

// MARK: Core Example Problem

/// A `MainActor`-isolated function that accepts non-`Sendable` parameters.
@MainActor
func applyBackground(_ color: ColorComponents) {
}

#if swift(<6.0)
/// A non-isolated function that accepts non-`Sendable` parameters.
func updateStyle(backgroundColor: ColorComponents) async {
    // the `backgroundColor` parameter is being moved from the
    // non-isolated domain to the `MainActor` here.
    //
    // Swift 5 Warning: passing argument of non-sendable type 'ColorComponents' into main actor-isolated context may introduce data races
    // Swift 6 Error: sending 'backgroundColor' risks causing data races
    await applyBackground(backgroundColor)
}
#endif

#if swift(>=6.0)
/// A non-isolated function that accepts non-`Sendable` parameters which must be safe to use at callsites.
func sending_updateStyle(backgroundColor: sending ColorComponents) async {
    await applyBackground(backgroundColor)
}
#endif

// MARK: Latent Isolation

/// MainActor-isolated function that accepts non-`Sendable` parameters.
@MainActor
func isolatedFunction_updateStyle(backgroundColor: ColorComponents) async {
    // This is safe because backgroundColor cannot change domains. It also
    // now no longer necessary to await the call to `applyBackground`.
    applyBackground(backgroundColor)
}

// MARK: Explicit Sendable

/// An overload used by `sendable_updateStyle` to match types.
@MainActor
func applyBackground(_ color: SendableColorComponents) {
}

/// The Sendable variant is safe to pass across isolation domains.
func sendable_updateStyle(backgroundColor: SendableColorComponents) async {
    await applyBackground(backgroundColor)
}

// MARK: Computed Value

/// A Sendable function is used to compute the value in a different isolation domain.
func computedValue_updateStyle(using backgroundColorProvider: @Sendable () -> ColorComponents) async {
    // The Swift 6 compiler can automatically determine this value is
    // being transferred in a safe way
    let components = backgroundColorProvider()
    await applyBackground(components)
}

#if swift(>=6.0)
/// A function that uses a sending parameter to leverage region-based isolation.
func sendingValue_updateStyle(backgroundColor: sending ColorComponents) async {
    await applyBackground(backgroundColor)
}
#endif

// MARK: Global Isolation
/// An overload used by `globalActorIsolated_updateStyle` to match types.
@MainActor
func applyBackground(_ color: GlobalActorIsolatedColorComponents) {
}

/// MainActor-isolated function that accepts non-`Sendable` parameters.
@MainActor
func globalActorIsolated_updateStyle(backgroundColor: GlobalActorIsolatedColorComponents) async {
    // This is safe because backgroundColor cannot change domains. It also
    // now no longer necessary to await the call to `applyBackground`.
    applyBackground(backgroundColor)
}

// MARK: actor isolation

/// An actor that assumes the responsibility of managing the non-Sendable data.
actor Style {
    private var background: ColorComponents

    init(background: ColorComponents) {
        self.background = background
    }

    func applyBackground() {
        // make use of background here
    }
}

// MARK: Manual Synchronization

extension RetroactiveColorComponents: @retroactive @unchecked Sendable {
}

/// An overload used by `retroactive_updateStyle` to match types.
@MainActor
func applyBackground(_ color: RetroactiveColorComponents	) {
}

/// A non-isolated function that accepts retroactively-`Sendable` parameters.
func retroactive_updateStyle(backgroundColor: RetroactiveColorComponents) async {
    await applyBackground(backgroundColor)
}

func exerciseBoundaryCrossingExamples() async {
    print("Isolation Boundary Crossing Examples")

#if swift(<6.0)
    print("  - updateStyle(backgroundColor:) passing its argument unsafely")
#endif

#if swift(>=6.0)
    print("  - using sending to allow safe usage of ColorComponents")
    let nonSendableComponents = ColorComponents()

    await sending_updateStyle(backgroundColor: nonSendableComponents)
#endif

    print("  - using ColorComponents only from the main actor")
    let t1 = Task { @MainActor in
        let components = ColorComponents()

        await isolatedFunction_updateStyle(backgroundColor: components)
    }

    await t1.value

    print("  - using preconcurrency_updateStyle to deal with non-Sendable argument")

    print("  - using a Sendable closure to defer creation")
    await computedValue_updateStyle(using: {
        ColorComponents()
    })

#if swift(>=6.0)
    print("  - enable region-based isolation with a sending argument")
    let capturableComponents = ColorComponents()

    await sendingValue_updateStyle(backgroundColor: capturableComponents)
#endif

    print("  - using a globally-isolated type")
    let components = await GlobalActorIsolatedColorComponents()

    await globalActorIsolated_updateStyle(backgroundColor: components)

    print("  - using an actor")
    let actorComponents = ColorComponents()

    let actor = Style(background: actorComponents)

    await actor.applyBackground()

    print("  - using a retroactive unchecked Sendable argument")
    let retroactiveComponents = RetroactiveColorComponents()

    await retroactive_updateStyle(backgroundColor: retroactiveComponents)
}



================================================
FILE: Sources/Examples/ConformanceMismatches.swift
================================================
import Library

// MARK: Under-Specified Protocol

#if swift(<6.0)
/// A conforming type that has now adopted global isolation.
@MainActor
class WindowStyler: Styler {
    // Swift 5 Warning: main actor-isolated instance method 'applyStyle()' cannot be used to satisfy nonisolated protocol requirement
    // Swift 6 Error: main actor-isolated instance method 'applyStyle()' cannot be used to satisfy nonisolated protocol requirement
    func applyStyle() {
    }
}
#endif

// MARK: Globally-Isolated Protocol

/// A type conforming to the global actor annotated `GloballyIsolatedStyler` protocol,
///  will infer the protocol's global actor isolation.
class GloballyIsolatedWindowStyler: GloballyIsolatedStyler {
    func applyStyle() {
    }
}

/// A type conforming to `PerRequirementIsolatedStyler` which has MainActor isolated protocol requirements,
/// will infer the protocol's requirements isolation for methods witnessing those protocol requirements *only*
/// for the satisfying methods.
class PerRequirementIsolatedWindowStyler: PerRequirementIsolatedStyler {
    func applyStyle() {
        // only this is MainActor-isolated
    }

    func checkStyle() {
        // this method is non-isolated; it is not witnessing any isolated protocol requirement
    }
}

// MARK: Asynchronous Requirements

/// A conforming type that can have arbitrary isolation and
/// still matches the async requirement.
class AsyncWindowStyler: AsyncStyler {
    func applyStyle() {
    }
}

// MARK: Using preconcurrency

/// A conforming type that will infer the protocol's global isolation *but*
/// with downgraded diagnostics in Swift 6 mode and Swift 5 + complete checking
class StagedGloballyIsolatedWindowStyler: StagedGloballyIsolatedStyler {
    func applyStyle() {
    }
}

// MARK: Using Dynamic Isolation

/// A conforming type that uses a nonisolated function to match
/// with dynamic isolation in the method body.
@MainActor
class DynamicallyIsolatedStyler: Styler {
    nonisolated func applyStyle() {
        MainActor.assumeIsolated {
            // MainActor state is available here
        }
    }
}

/// A conforming type that uses a preconcurency conformance, which
/// is a safer and more ergonomic version of DynamicallyIsolatedStyler.
@MainActor
class PreconcurrencyConformanceStyler: @preconcurrency Styler {
    func applyStyle() {
    }
}

// MARK: Non-Isolated

/// A conforming type that uses nonisolated and non-Sendable types but
/// still performs useful work.
@MainActor
class NonisolatedWindowStyler: StylerConfiguration {
    nonisolated var primaryColorComponents: ColorComponents {
        ColorComponents(red: 0.2, green: 0.3, blue: 0.4)
    }
}

// MARK: Conformance by Proxy

/// An intermediary type that conforms to the protocol so it can be
/// used by an actor
struct CustomWindowStyle: Styler {
    func applyStyle() {
    }
}

/// An actor that interacts with the Style protocol indirectly.
actor ActorWindowStyler {
    private let internalStyle = CustomWindowStyle()

    func applyStyle() {
        // forward the call through to the conforming type
        internalStyle.applyStyle()
    }
}

func exerciseConformanceMismatchExamples() async {
    print("Protocol Conformance Isolation Mismatch Examples")

    // Could also all be done with async calls, but this
    // makes the isolation, and the ability to invoke them
    // from a synchronous context explicit.
    await MainActor.run {
#if swift(<6.0)
        print("  - using a mismatched conformance")
        WindowStyler().applyStyle()
#endif

        print("  - using a MainActor-isolated type")
        GloballyIsolatedWindowStyler().applyStyle()

        print("  - using a per-requirement MainActor-isolated type")
        PerRequirementIsolatedWindowStyler().applyStyle()

        print("  - using an async conformance")
        AsyncWindowStyler().applyStyle()

        print("  - using staged isolation")
        StagedGloballyIsolatedWindowStyler().applyStyle()

        print("  - using dynamic isolation")
        DynamicallyIsolatedStyler().applyStyle()

        print("  - using a preconcurrency conformance")
        PreconcurrencyConformanceStyler().applyStyle()

        let value = NonisolatedWindowStyler().primaryColorComponents
        print("  - accessing a non-isolated conformance: ", value)
    }

    print("  - using an actor with a proxy conformance")
    await ActorWindowStyler().applyStyle()
}



================================================
FILE: Sources/Examples/DispatchQueue+PendingWork.swift
================================================
import Dispatch

extension DispatchQueue {
    /// Returns once any pending work has been completed.
    func pendingWorkComplete() async {
        // TODO: update to withCheckedContinuation https://github.com/apple/swift/issues/74206
        await withUnsafeContinuation { continuation in
            self.async(flags: .barrier) {
                continuation.resume()
            }
        }
    }
}



================================================
FILE: Sources/Examples/Globals.swift
================================================
import Dispatch

#if swift(<6.0)
/// An unsafe global variable.
///
/// See swift-6-concurrency-migration-guide/commonproblems/#Sendable-Types
var supportedStyleCount = 42
#endif

/// Version of `supportedStyleCount` that uses global-actor isolation.
@MainActor
var globallyIsolated_supportedStyleCount = 42

/// Version of `supportedStyleCount` that uses immutability.
let constant_supportedStyleCount = 42

/// Version of `supportedStyleCount` that uses a computed property.
var computed_supportedStyleCount: Int {
    42
}

/// Version of `supportedStyleCount` that uses manual synchronization via `sharedQueue`
nonisolated(unsafe) var queueProtected_supportedStyleCount = 42

/// A non-isolated async function used to exercise all of the global mutable state examples.
func exerciseGlobalExamples() async {
    print("Global Variable Examples")
#if swift(<6.0)
    // Here is how we access `supportedStyleCount` concurrently in an unsafe way
    for _ in 0..<10 {
        DispatchQueue.global().async {
            supportedStyleCount += 1
        }
    }

    print("  - accessing supportedStyleCount unsafely:", supportedStyleCount)

    await DispatchQueue.global().pendingWorkComplete()
#endif
    
    print("  - accessing globallyIsolated_supportedStyleCount")
    // establish a MainActor context to access the globally-isolated version
    await MainActor.run {
        globallyIsolated_supportedStyleCount += 1
    }

    // freely access the immutable version from any isolation domain
    print("  - accessing constant_supportedStyleCount when non-isolated: ", constant_supportedStyleCount)

    await MainActor.run {
        print("  - accessing constant_supportedStyleCount from MainActor: ", constant_supportedStyleCount)
    }

    // freely access the computed property from any isolation domain
    print("  - accessing computed_supportedStyleCount when non-isolated: ", computed_supportedStyleCount)

    // access the manually-synchronized version... carefully
    manualSerialQueue.async {
        queueProtected_supportedStyleCount += 1
    }

    manualSerialQueue.async {
        print("  - accessing queueProtected_supportedStyleCount: ", queueProtected_supportedStyleCount)
    }

    await manualSerialQueue.pendingWorkComplete()
}



================================================
FILE: Sources/Examples/IncrementalMigration.swift
================================================
import Dispatch
import ObjCLibrary

/// Example that backs an actor with a queue.
///
/// > Note: `DispatchSerialQueue`'s initializer was only made available in more recent OS versions.
@available(macOS 14.0, iOS 17.0, macCatalyst 17.0, tvOS 17.0, watchOS 10.0, *)
actor LandingSite {
    private let queue = DispatchSerialQueue(label: "SerialQueue")

	// this currently failed to build because of the @available usage, rdar://116684282
//    nonisolated var unownedExecutor: UnownedSerialExecutor {
//        queue.asUnownedSerialExecutor()
//    }

    func acceptTransport(_ transport: JPKJetPack) {
        // this function will be running on queue
    }
}

func exerciseIncrementalMigrationExamples() async {
    print("Incremental Migration Examples")

    if #available(macOS 14.0, iOS 17.0, macCatalyst 17.0, tvOS 17.0, watchOS 10.0, *) {
        print("  - using an actor with a DispatchSerialQueue executor")
        let site = LandingSite()

        let transport = JPKJetPack()

        await site.acceptTransport(transport)
    }
}



================================================
FILE: Sources/Examples/main.swift
================================================
import Dispatch

/// A Serial queue uses for manual synchronization
let manualSerialQueue = DispatchQueue(label: "com.apple.SwiftMigrationGuide")

// Note: top-level code provides an asynchronous MainActor-isolated context
await exerciseGlobalExamples()
await exerciseBoundaryCrossingExamples()
await exerciseConformanceMismatchExamples()
await exerciseIncrementalMigrationExamples()



================================================
FILE: Sources/Examples/PreconcurrencyImport.swift
================================================
@preconcurrency import Library

/// A non-isolated function  that accepts non-`Sendable` parameters.
func preconcurrency_updateStyle(backgroundColor: ColorComponents) async {
    // Swift 5: no diagnostics
    // Swift 6 Warning: sending 'backgroundColor' risks causing data races
    await applyBackground(backgroundColor)
}



================================================
FILE: Sources/Library/Library.swift
================================================
import Foundation

/// An example of a struct with only `Sendable` properties.
///
/// This type is **not** Sendable because it is public. If we want a public type to be `Sendable`, we must annotate it explicitly.
public struct ColorComponents {
    public let red: Float
    public let green: Float
    public let blue: Float

    public init(red: Float, green: Float, blue: Float) {
        self.red = red
        self.green = green
        self.blue = blue
    }

    public init() {
        self.red = 1.0
        self.green = 1.0
        self.blue = 1.0
    }
}

/// A variant of `ColorComponents` that could be marked as Sendable
public struct RetroactiveColorComponents {
    public let red: Float = 1.0
    public let green: Float = 1.0
    public let blue: Float = 1.0

    public init() {}
}

/// Explicitly-Sendable variant of `ColorComponents`.
public struct SendableColorComponents : Sendable {
    public let red: Float = 1.0
    public let green: Float = 1.0
    public let blue: Float = 1.0

    public init() {}
}

@MainActor
public struct GlobalActorIsolatedColorComponents : Sendable {
    public let red: Float = 1.0
    public let green: Float = 1.0
    public let blue: Float = 1.0

    public init() {}
}

public protocol Styler {
    func applyStyle()
}

@MainActor
public protocol GloballyIsolatedStyler {
    func applyStyle()
}

public protocol PerRequirementIsolatedStyler {
    @MainActor
    func applyStyle()
}

@preconcurrency @MainActor
public protocol StagedGloballyIsolatedStyler {
    func applyStyle()
}

public protocol AsyncStyler {
    func applyStyle() async
}

open class UIStyler {
}

public protocol InheritingStyler: UIStyler {
    func applyStyle()
}

public protocol StylerConfiguration {
    var primaryColorComponents: ColorComponents { get }
}



================================================
FILE: Sources/ObjCLibrary/JPKJetPack.h
================================================
#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface JPKJetPack : NSObject

/// Disable async to show how completion handlers work explicitly.
+ (void)jetPackConfiguration:(void (NS_SWIFT_SENDABLE ^)(void))completionHandler NS_SWIFT_DISABLE_ASYNC;

@end

NS_ASSUME_NONNULL_END



================================================
FILE: Sources/ObjCLibrary/JPKJetPack.m
================================================
#import "JPKJetPack.h"

@implementation JPKJetPack

+ (void)jetPackConfiguration:(void (^)(void))completionHandler {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        completionHandler();
    });
}

@end



================================================
FILE: Sources/ObjCLibrary/ObjCLibrary.h
================================================
@import Foundation;

@interface OCMPattern : NSObject

@end

NS_SWIFT_UI_ACTOR
@interface PCMPatternStore : NSObject

@end

#import "JPKJetPack.h"



================================================
FILE: Sources/ObjCLibrary/ObjCLibrary.m
================================================
#import <Foundation/Foundation.h>

#import "ObjCLibrary.h"

@implementation OCMPattern

@end

@implementation PCMPatternStore

@end



================================================
SYMLINK: Sources/Swift5Examples -> Examples
================================================



================================================
SYMLINK: Sources/Swift6Examples -> Examples
================================================



================================================
FILE: Tests/Library/LibraryTests.swift
================================================
import Library
import ObjCLibrary
import Testing

struct LibraryTest {
    @Test func testNonIsolated() throws {
        let color = ColorComponents()

        #expect(color.red == 1.0)
    }

    @MainActor
    @Test func testIsolated() throws {
        let color = GlobalActorIsolatedColorComponents()

        #expect(color.red == 1.0)
    }

    @Test func testNonIsolatedWithGlobalActorIsolatedType() async throws {
        let color = await GlobalActorIsolatedColorComponents()

        await #expect(color.red == 1.0)
    }
}

extension LibraryTest {
    @Test func testCallbackOperation() async {
        await confirmation() { completion in
            // function explicitly opts out of an generated async version
            // so it requires a continuation here
            await withCheckedContinuation { continuation in
                JPKJetPack.jetPackConfiguration {
                    completion()
                    continuation.resume()
                }
            }
        }
    }
}



================================================
FILE: Tests/Library/LibraryXCTests.swift
================================================
import ObjCLibrary
import Library
import XCTest

final class LibraryXCTests: XCTestCase {
    func testNonIsolated() throws {
        let color = ColorComponents()

        XCTAssertEqual(color.red, 1.0)
    }

    @MainActor
    func testIsolated() throws {
        let color = GlobalActorIsolatedColorComponents()

        XCTAssertEqual(color.red, 1.0)
    }

    func testNonIsolatedWithGlobalActorIsolatedType() async throws {
        let color = await GlobalActorIsolatedColorComponents()
        let redComponent = await color.red

        XCTAssertEqual(redComponent, 1.0)
    }
}

extension LibraryXCTests {
    func testCallbackOperation() async {
        let exp = expectation(description: "config callback")

        JPKJetPack.jetPackConfiguration {
            exp.fulfill()
        }

        await fulfillment(of: [exp])
    }
}