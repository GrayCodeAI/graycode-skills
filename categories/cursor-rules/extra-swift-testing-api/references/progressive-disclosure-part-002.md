[`struct ParallelizationTrait`](https://developer.apple.com/documentation/testing/parallelizationtrait)

A type that defines whether the testing library runs this test serially or in parallel.

[`struct Tag`](https://developer.apple.com/documentation/testing/tag)

A type representing a tag that can be applied to a test.

[`struct List`](https://developer.apple.com/documentation/testing/tag/list)

A type representing one or more tags applied to a test.

[`struct TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait)

A type that defines a time limit to apply to a test.

Current page is Traits

## Custom Test String
[Skip Navigation](https://developer.apple.com/documentation/testing/customteststringconvertible#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- CustomTestStringConvertible

Protocol

# CustomTestStringConvertible

A protocol describing types with a custom string representation when presented as part of a test’s output.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
protocol CustomTestStringConvertible
```

## [Overview](https://developer.apple.com/documentation/testing/customteststringconvertible\#overview)

Values whose types conform to this protocol use it to describe themselves when they are present as part of the output of a test. For example, this protocol affects the display of values that are passed as arguments to test functions or that are elements of an expectation failure.

By default, the testing library converts values to strings using `String(describing:)`. The resulting string may be inappropriate for some types and their values. If the type of the value is made to conform to [`CustomTestStringConvertible`](https://developer.apple.com/documentation/testing/customteststringconvertible), then the value of its [`testDescription`](https://developer.apple.com/documentation/testing/customteststringconvertible/testdescription) property will be used instead.

For example, consider the following type:

```
enum Food: CaseIterable {
  case paella, oden, ragu
}

```

If an array of cases from this enumeration is passed to a parameterized test function:

```
@Test(arguments: Food.allCases)
func isDelicious(_ food: Food) { ... }

```

Then the values in the array need to be presented in the test output, but the default description of a value may not be adequately descriptive:

```
◇ Passing argument food → .paella to isDelicious(_:)
◇ Passing argument food → .oden to isDelicious(_:)
◇ Passing argument food → .ragu to isDelicious(_:)

```

By adopting [`CustomTestStringConvertible`](https://developer.apple.com/documentation/testing/customteststringconvertible), customized descriptions can be included:

```
extension Food: CustomTestStringConvertible {
  var testDescription: String {
    switch self {
    case .paella:
      "paella valenciana"
    case .oden:
      "おでん"
    case .ragu:
      "ragù alla bolognese"
    }
  }
}

```

The presentation of these values will then reflect the value of the [`testDescription`](https://developer.apple.com/documentation/testing/customteststringconvertible/testdescription) property:

```
◇ Passing argument food → paella valenciana to isDelicious(_:)
◇ Passing argument food → おでん to isDelicious(_:)
◇ Passing argument food → ragù alla bolognese to isDelicious(_:)

```

## [Topics](https://developer.apple.com/documentation/testing/customteststringconvertible\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/customteststringconvertible\#Instance-Properties)

[`var testDescription: String`](https://developer.apple.com/documentation/testing/customteststringconvertible/testdescription)

A description of this instance to use when presenting it in a test’s output.

**Required** Default implementation provided.

## [See Also](https://developer.apple.com/documentation/testing/customteststringconvertible\#see-also)

### [Retrieving information about checked expectations](https://developer.apple.com/documentation/testing/customteststringconvertible\#Retrieving-information-about-checked-expectations)

[`struct Expectation`](https://developer.apple.com/documentation/testing/expectation)

A type describing an expectation that has been evaluated.

[`struct ExpectationFailedError`](https://developer.apple.com/documentation/testing/expectationfailederror)

A type describing an error thrown when an expectation fails during evaluation.

Current page is CustomTestStringConvertible

## Swift Testing Issues
[Skip Navigation](https://developer.apple.com/documentation/testing/issue#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Issue

Structure

# Issue

A type describing a failure or warning which occurred during a test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct Issue
```

## [Mentioned in](https://developer.apple.com/documentation/testing/issue\#mentions)

[Associating bugs with tests](https://developer.apple.com/documentation/testing/associatingbugs)

[Interpreting bug identifiers](https://developer.apple.com/documentation/testing/bugidentifiers)

## [Topics](https://developer.apple.com/documentation/testing/issue\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/issue\#Instance-Properties)

[`var comments: [Comment]`](https://developer.apple.com/documentation/testing/issue/comments)

Any comments provided by the developer and associated with this issue.

[`var error: (any Error)?`](https://developer.apple.com/documentation/testing/issue/error)

The error which was associated with this issue, if any.

[`var kind: Issue.Kind`](https://developer.apple.com/documentation/testing/issue/kind-swift.property)

The kind of issue this value represents.

[`var sourceLocation: SourceLocation?`](https://developer.apple.com/documentation/testing/issue/sourcelocation)

The location in source where this issue occurred, if available.

### [Type Methods](https://developer.apple.com/documentation/testing/issue\#Type-Methods)

[`static func record(any Error, Comment?, sourceLocation: SourceLocation) -> Issue`](https://developer.apple.com/documentation/testing/issue/record(_:_:sourcelocation:))

Record a new issue when a running test unexpectedly catches an error.

[`static func record(Comment?, sourceLocation: SourceLocation) -> Issue`](https://developer.apple.com/documentation/testing/issue/record(_:sourcelocation:))

Record an issue when a running test fails unexpectedly.

### [Enumerations](https://developer.apple.com/documentation/testing/issue\#Enumerations)

[`enum Kind`](https://developer.apple.com/documentation/testing/issue/kind-swift.enum)

Kinds of issues which may be recorded.

### [Default Implementations](https://developer.apple.com/documentation/testing/issue\#Default-Implementations)

[API Reference\\
CustomDebugStringConvertible Implementations](https://developer.apple.com/documentation/testing/issue/customdebugstringconvertible-implementations)

[API Reference\\
CustomStringConvertible Implementations](https://developer.apple.com/documentation/testing/issue/customstringconvertible-implementations)

## [Relationships](https://developer.apple.com/documentation/testing/issue\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/issue\#conforms-to)

- [`Copyable`](https://developer.apple.com/documentation/Swift/Copyable)
- [`CustomDebugStringConvertible`](https://developer.apple.com/documentation/Swift/CustomDebugStringConvertible)
- [`CustomStringConvertible`](https://developer.apple.com/documentation/Swift/CustomStringConvertible)
- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)

Current page is Issue

## Migrating from XCTest
[Skip Navigation](https://developer.apple.com/documentation/testing/migratingfromxctest#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Migrating a test from XCTest

Article

# Migrating a test from XCTest

Migrate an existing test method or test class written using XCTest.

## [Overview](https://developer.apple.com/documentation/testing/migratingfromxctest\#Overview)

The testing library provides much of the same functionality of XCTest, but uses its own syntax to declare test functions and types. Here, you’ll learn how to convert XCTest-based content to use the testing library instead.

### [Import the testing library](https://developer.apple.com/documentation/testing/migratingfromxctest\#Import-the-testing-library)

XCTest and the testing library are available from different modules. Instead of importing the XCTest module, import the Testing module:

```
// Before
import XCTest

```

```
// After
import Testing

```

A single source file can contain tests written with XCTest as well as other tests written with the testing library. Import both XCTest and Testing if a source file contains mixed test content.

### [Convert test classes](https://developer.apple.com/documentation/testing/migratingfromxctest\#Convert-test-classes)

XCTest groups related sets of test methods in test classes: classes that inherit from the [`XCTestCase`](https://developer.apple.com/documentation/xctest/xctestcase) class provided by the [XCTest](https://developer.apple.com/documentation/xctest) framework. The testing library doesn’t require that test functions be instance members of types. Instead, they can be _free_ or _global_ functions, or can be `static` or `class` members of a type.

If you want to group your test functions together, you can do so by placing them in a Swift type. The testing library refers to such a type as a _suite_. These types do _not_ need to be classes, and they don’t inherit from `XCTestCase`.

To convert a subclass of `XCTestCase` to a suite, remove the `XCTestCase` conformance. It’s also generally recommended that a Swift structure or actor be used instead of a class because it allows the Swift compiler to better-enforce concurrency safety:

```
// Before
class FoodTruckTests: XCTestCase {
  ...
}

```

```
// After
struct FoodTruckTests {
  ...
}

```

For more information about suites and how to declare and customize them, see [Organizing test functions with suite types](https://developer.apple.com/documentation/testing/organizingtests).

### [Convert setup and teardown functions](https://developer.apple.com/documentation/testing/migratingfromxctest\#Convert-setup-and-teardown-functions)

In XCTest, code can be scheduled to run before and after a test using the [`setUp()`](https://developer.apple.com/documentation/xctest/xctest/3856481-setup) and [`tearDown()`](https://developer.apple.com/documentation/xctest/xctest/3856482-teardown) family of functions. When writing tests using the testing library, implement `init()` and/or `deinit` instead:

```
// Before
class FoodTruckTests: XCTestCase {
  var batteryLevel: NSNumber!
  override func setUp() async throws {
    batteryLevel = 100
  }
  ...
}

```

```
// After
struct FoodTruckTests {
  var batteryLevel: NSNumber
  init() async throws {
    batteryLevel = 100
  }
  ...
}

```

The use of `async` and `throws` is optional. If teardown is needed, declare your test suite as a class or as an actor rather than as a structure and implement `deinit`:

```
// Before
class FoodTruckTests: XCTestCase {
  var batteryLevel: NSNumber!
  override func setUp() async throws {
    batteryLevel = 100
  }
  override func tearDown() {
    batteryLevel = 0 // drain the battery
  }
  ...
}

```

```
// After
final class FoodTruckTests {
  var batteryLevel: NSNumber
  init() async throws {
    batteryLevel = 100
  }
  deinit {
    batteryLevel = 0 // drain the battery
  }
  ...
}

```

### [Convert test methods](https://developer.apple.com/documentation/testing/migratingfromxctest\#Convert-test-methods)

The testing library represents individual tests as functions, similar to how they are represented in XCTest. However, the syntax for declaring a test function is different. In XCTest, a test method must be a member of a test class and its name must start with `test`. The testing library doesn’t require a test function to have any particular name. Instead, it identifies a test function by the presence of the `@Test` attribute:

```
// Before
class FoodTruckTests: XCTestCase {
  func testEngineWorks() { ... }
  ...
}

```

```
// After
struct FoodTruckTests {
  @Test func engineWorks() { ... }
  ...
}

```

As with XCTest, the testing library allows test functions to be marked `async`, `throws`, or `async`- `throws`, and to be isolated to a global actor (for example, by using the `@MainActor` attribute.)

For more information about test functions and how to declare and customize them, see [Defining test functions](https://developer.apple.com/documentation/testing/definingtests).

### [Check for expected values and outcomes](https://developer.apple.com/documentation/testing/migratingfromxctest\#Check-for-expected-values-and-outcomes)

XCTest uses a family of approximately 40 functions to assert test requirements. These functions are collectively referred to as [`XCTAssert()`](https://developer.apple.com/documentation/xctest/1500669-xctassert). The testing library has two replacements, [`expect(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:)) and [`require(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q). They both behave similarly to `XCTAssert()` except that [`require(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q) throws an error if its condition isn’t met:

```
// Before
func testEngineWorks() throws {
  let engine = FoodTruck.shared.engine
  XCTAssertNotNil(engine.parts.first)
  XCTAssertGreaterThan(engine.batteryLevel, 0)
  try engine.start()
  XCTAssertTrue(engine.isRunning)
}

```

```
// After
@Test func engineWorks() throws {
  let engine = FoodTruck.shared.engine
  try #require(engine.parts.first != nil)
  #expect(engine.batteryLevel > 0)
  try engine.start()
  #expect(engine.isRunning)
}

```

### [Check for optional values](https://developer.apple.com/documentation/testing/migratingfromxctest\#Check-for-optional-values)

XCTest also has a function, [`XCTUnwrap()`](https://developer.apple.com/documentation/xctest/3380195-xctunwrap), that tests if an optional value is `nil` and throws an error if it is. When using the testing library, you can use [`require(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-6w9oo) with optional expressions to unwrap them:

```
// Before
func testEngineWorks() throws {
  let engine = FoodTruck.shared.engine
  let part = try XCTUnwrap(engine.parts.first)
  ...
}

```

```
// After
@Test func engineWorks() throws {
  let engine = FoodTruck.shared.engine
  let part = try #require(engine.parts.first)
  ...
}

```

### [Record issues](https://developer.apple.com/documentation/testing/migratingfromxctest\#Record-issues)

XCTest has a function, [`XCTFail()`](https://developer.apple.com/documentation/xctest/1500970-xctfail), that causes a test to fail immediately and unconditionally. This function is useful when the syntax of the language prevents the use of an `XCTAssert()` function. To record an unconditional issue using the testing library, use the [`record(_:sourceLocation:)`](https://developer.apple.com/documentation/testing/issue/record(_:sourcelocation:)) function:

```
// Before
func testEngineWorks() {
  let engine = FoodTruck.shared.engine
  guard case .electric = engine else {
    XCTFail("Engine is not electric")
    return
  }
  ...
}

```

```
// After
@Test func engineWorks() {
  let engine = FoodTruck.shared.engine
  guard case .electric = engine else {
    Issue.record("Engine is not electric")
    return
  }
  ...
}

```

The following table includes a list of the various `XCTAssert()` functions and their equivalents in the testing library:

| XCTest | Swift Testing |
| --- | --- |
| `XCTAssert(x)`, `XCTAssertTrue(x)` | `#expect(x)` |
| `XCTAssertFalse(x)` | `#expect(!x)` |
| `XCTAssertNil(x)` | `#expect(x == nil)` |
| `XCTAssertNotNil(x)` | `#expect(x != nil)` |
| `XCTAssertEqual(x, y)` | `#expect(x == y)` |
| `XCTAssertNotEqual(x, y)` | `#expect(x != y)` |
| `XCTAssertIdentical(x, y)` | `#expect(x === y)` |
| `XCTAssertNotIdentical(x, y)` | `#expect(x !== y)` |
| `XCTAssertGreaterThan(x, y)` | `#expect(x > y)` |
| `XCTAssertGreaterThanOrEqual(x, y)` | `#expect(x >= y)` |
| `XCTAssertLessThanOrEqual(x, y)` | `#expect(x <= y)` |
| `XCTAssertLessThan(x, y)` | `#expect(x < y)` |
| `XCTAssertThrowsError(try f())` | `#expect(throws: (any Error).self) { try f() }` |
| `XCTAssertThrowsError(try f()) { error in … }` | `let error = #expect(throws: (any Error).self) { try f() }` |
| `XCTAssertNoThrow(try f())` | `#expect(throws: Never.self) { try f() }` |
| `try XCTUnwrap(x)` | `try #require(x)` |
| `XCTFail("…")` | `Issue.record("…")` |

The testing library doesn’t provide an equivalent of [`XCTAssertEqual(_:_:accuracy:_:file:line:)`](https://developer.apple.com/documentation/xctest/3551607-xctassertequal). To compare two numeric values within a specified accuracy, use `isApproximatelyEqual()` from [swift-numerics](https://github.com/apple/swift-numerics).

### [Continue or halt after test failures](https://developer.apple.com/documentation/testing/migratingfromxctest\#Continue-or-halt-after-test-failures)

An instance of an `XCTestCase` subclass can set its [`continueAfterFailure`](https://developer.apple.com/documentation/xctest/xctestcase/1496260-continueafterfailure) property to `false` to cause a test to stop running after a failure occurs. XCTest stops an affected test by throwing an Objective-C exception at the time the failure occurs.

The behavior of an exception thrown through a Swift stack frame is undefined. If an exception is thrown through an `async` Swift function, it typically causes the process to terminate abnormally, preventing other tests from running.

The testing library doesn’t use exceptions to stop test functions. Instead, use the [`require(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q) macro, which throws a Swift error on failure:

```
// Before
func testTruck() async {
  continueAfterFailure = false
  XCTAssertTrue(FoodTruck.shared.isLicensed)
  ...
}

```

```
// After
@Test func truck() throws {
  try #require(FoodTruck.shared.isLicensed)
  ...
}

```

When using either `continueAfterFailure` or [`require(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q), other tests will continue to run after the failed test method or test function.

### [Validate asynchronous behaviors](https://developer.apple.com/documentation/testing/migratingfromxctest\#Validate-asynchronous-behaviors)

XCTest has a class, [`XCTestExpectation`](https://developer.apple.com/documentation/xctest/xctestexpectation), that represents some asynchronous condition. You create an instance of this class (or a subclass like [`XCTKeyPathExpectation`](https://developer.apple.com/documentation/xctest/xctkeypathexpectation)) using an initializer or a convenience method on `XCTestCase`. When the condition represented by an expectation occurs, the developer _fulfills_ the expectation. Concurrently, the developer _waits for_ the expectation to be fulfilled using an instance of [`XCTWaiter`](https://developer.apple.com/documentation/xctest/xctwaiter) or using a convenience method on `XCTestCase`.

Wherever possible, prefer to use Swift concurrency to validate asynchronous conditions. For example, if it’s necessary to determine the result of an asynchronous Swift function, it can be awaited with `await`. For a function that takes a completion handler but which doesn’t use `await`, a Swift [continuation](https://developer.apple.com/documentation/swift/withcheckedcontinuation(function:_:)) can be used to convert the call into an `async`-compatible one.

Some tests, especially those that test asynchronously-delivered events, cannot be readily converted to use Swift concurrency. The testing library offers functionality called _confirmations_ which can be used to implement these tests. Instances of [`Confirmation`](https://developer.apple.com/documentation/testing/confirmation) are created and used within the scope of the functions [`confirmation(_:expectedCount:isolation:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-5mqz2) and [`confirmation(_:expectedCount:isolation:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-l3il).

Confirmations function similarly to the expectations API of XCTest, however, they don’t block or suspend the caller while waiting for a condition to be fulfilled. Instead, the requirement is expected to be _confirmed_ (the equivalent of _fulfilling_ an expectation) before `confirmation()` returns, and records an issue otherwise:

```
// Before
func testTruckEvents() async {
  let soldFood = expectation(description: "…")
  FoodTruck.shared.eventHandler = { event in
    if case .soldFood = event {
      soldFood.fulfill()
    }
  }
  await Customer().buy(.soup)
  await fulfillment(of: [soldFood])
  ...
}

```

```
// After
@Test func truckEvents() async {
  await confirmation("…") { soldFood in
    FoodTruck.shared.eventHandler = { event in
      if case .soldFood = event {
        soldFood()
      }
    }
    await Customer().buy(.soup)
  }
  ...
}

```

By default, `XCTestExpectation` expects to be fulfilled exactly once, and will record an issue in the current test if it is not fulfilled or if it is fulfilled more than once. `Confirmation` behaves the same way and expects to be confirmed exactly once by default. You can configure the number of times an expectation should be fulfilled by setting its [`expectedFulfillmentCount`](https://developer.apple.com/documentation/xctest/xctestexpectation/2806572-expectedfulfillmentcount) property, and you can pass a value for the `expectedCount` argument of [`confirmation(_:expectedCount:isolation:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-5mqz2) for the same purpose.

`XCTestExpectation` has a property, [`assertForOverFulfill`](https://developer.apple.com/documentation/xctest/xctestexpectation/2806575-assertforoverfulfill), which when set to `false` allows an expectation to be fulfilled more times than expected without causing a test failure. When using a confirmation, you can pass a range to [`confirmation(_:expectedCount:isolation:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-l3il) as its expected count to indicate that it must be confirmed _at least_ some number of times:

```
// Before
func testRegularCustomerOrders() async {
  let soldFood = expectation(description: "…")
  soldFood.expectedFulfillmentCount = 10
  soldFood.assertForOverFulfill = false
  FoodTruck.shared.eventHandler = { event in
    if case .soldFood = event {
      soldFood.fulfill()
    }
  }
  for customer in regularCustomers() {
    await customer.buy(customer.regularOrder)
  }
  await fulfillment(of: [soldFood])
  ...
}

```

```
// After
@Test func regularCustomerOrders() async {
  await confirmation(
    "…",
    expectedCount: 10...
  ) { soldFood in
    FoodTruck.shared.eventHandler = { event in
      if case .soldFood = event {
        soldFood()
      }
    }
    for customer in regularCustomers() {
      await customer.buy(customer.regularOrder)
    }
  }
  ...
}

```

Any range expression with a lower bound (that is, whose type conforms to both [`RangeExpression<Int>`](https://developer.apple.com/documentation/swift/rangeexpression) and [`Sequence<Int>`](https://developer.apple.com/documentation/swift/sequence)) can be used with [`confirmation(_:expectedCount:isolation:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-l3il). You must specify a lower bound for the number of confirmations because, without one, the testing library cannot tell if an issue should be recorded when there have been zero confirmations.

### [Control whether a test runs](https://developer.apple.com/documentation/testing/migratingfromxctest\#Control-whether-a-test-runs)

When using XCTest, the [`XCTSkip`](https://developer.apple.com/documentation/xctest/xctskip) error type can be thrown to bypass the remainder of a test function. As well, the [`XCTSkipIf()`](https://developer.apple.com/documentation/xctest/3521325-xctskipif) and [`XCTSkipUnless()`](https://developer.apple.com/documentation/xctest/3521326-xctskipunless) functions can be used to conditionalize the same action. The testing library allows developers to skip a test function or an entire test suite before it starts running using the [`ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait) trait type. Annotate a test suite or test function with an instance of this trait type to control whether it runs:

```
// Before
class FoodTruckTests: XCTestCase {
  func testArepasAreTasty() throws {
    try XCTSkipIf(CashRegister.isEmpty)
    try XCTSkipUnless(FoodTruck.sells(.arepas))
    ...
  }
  ...
}

```

```
// After
@Suite(.disabled(if: CashRegister.isEmpty))
struct FoodTruckTests {
  @Test(.enabled(if: FoodTruck.sells(.arepas)))
  func arepasAreTasty() {
    ...
  }
  ...
}

```

### [Annotate known issues](https://developer.apple.com/documentation/testing/migratingfromxctest\#Annotate-known-issues)

A test may have a known issue that sometimes or always prevents it from passing. When written using XCTest, such tests can call [`XCTExpectFailure(_:options:failingBlock:)`](https://developer.apple.com/documentation/xctest/3727246-xctexpectfailure) to tell XCTest and its infrastructure that the issue shouldn’t cause the test to fail. The testing library has an equivalent function with synchronous and asynchronous variants:

- [`withKnownIssue(_:isIntermittent:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:))

- [`withKnownIssue(_:isIntermittent:isolation:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:isolation:sourcelocation:_:))


This function can be used to annotate a section of a test as having a known issue:

```
// Before
func testGrillWorks() async {
  XCTExpectFailure("Grill is out of fuel") {
    try FoodTruck.shared.grill.start()
  }
  ...
}

```

```
// After
@Test func grillWorks() async {
  withKnownIssue("Grill is out of fuel") {
    try FoodTruck.shared.grill.start()
  }
  ...
}

```

If a test may fail intermittently, the call to `XCTExpectFailure(_:options:failingBlock:)` can be marked _non-strict_. When using the testing library, specify that the known issue is _intermittent_ instead:

```
// Before
func testGrillWorks() async {
  XCTExpectFailure(
    "Grill may need fuel",
    options: .nonStrict()
  ) {
    try FoodTruck.shared.grill.start()
  }
  ...
}

```

```
// After
@Test func grillWorks() async {
  withKnownIssue(
    "Grill may need fuel",
    isIntermittent: true
  ) {
    try FoodTruck.shared.grill.start()
  }
  ...
}

```

Additional options can be specified when calling `XCTExpectFailure()`:

- [`isEnabled`](https://developer.apple.com/documentation/xctest/xctexpectedfailure/options/3726085-isenabled) can be set to `false` to skip known-issue matching (for instance, if a particular issue only occurs under certain conditions)

- [`issueMatcher`](https://developer.apple.com/documentation/xctest/xctexpectedfailure/options/3726086-issuematcher) can be set to a closure to allow marking only certain issues as known and to allow other issues to be recorded as test failures


The testing library includes overloads of `withKnownIssue()` that take additional arguments with similar behavior:

- [`withKnownIssue(_:isIntermittent:sourceLocation:_:when:matching:)`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:when:matching:))

- [`withKnownIssue(_:isIntermittent:isolation:sourceLocation:_:when:matching:)`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:isolation:sourcelocation:_:when:matching:))


To conditionally enable known-issue matching or to match only certain kinds of issues:

```
// Before
func testGrillWorks() async {
  let options = XCTExpectedFailure.Options()
  options.isEnabled = FoodTruck.shared.hasGrill
  options.issueMatcher = { issue in
    issue.type == thrownError
  }
  XCTExpectFailure(
    "Grill is out of fuel",
    options: options
  ) {
    try FoodTruck.shared.grill.start()
  }
  ...
}

```

```
// After
@Test func grillWorks() async {
  withKnownIssue("Grill is out of fuel") {
    try FoodTruck.shared.grill.start()
  } when: {
    FoodTruck.shared.hasGrill
  } matching: { issue in
    issue.error != nil
  }
  ...
}

```

### [Run tests sequentially](https://developer.apple.com/documentation/testing/migratingfromxctest\#Run-tests-sequentially)

By default, the testing library runs all tests in a suite in parallel. The default behavior of XCTest is to run each test in a suite sequentially. If your tests use shared state such as global variables, you may see unexpected behavior including unreliable test outcomes when you run tests in parallel.

Annotate your test suite with [`serialized`](https://developer.apple.com/documentation/testing/trait/serialized) to run tests within that suite serially:

```
// Before
class RefrigeratorTests : XCTestCase {
  func testLightComesOn() throws {
    try FoodTruck.shared.refrigerator.openDoor()
    XCTAssertEqual(FoodTruck.shared.refrigerator.lightState, .on)
  }

  func testLightGoesOut() throws {
    try FoodTruck.shared.refrigerator.openDoor()
    try FoodTruck.shared.refrigerator.closeDoor()
    XCTAssertEqual(FoodTruck.shared.refrigerator.lightState, .off)
  }
}

```

```
// After
@Suite(.serialized)
class RefrigeratorTests {
  @Test func lightComesOn() throws {
    try FoodTruck.shared.refrigerator.openDoor()
    #expect(FoodTruck.shared.refrigerator.lightState == .on)
  }

  @Test func lightGoesOut() throws {
    try FoodTruck.shared.refrigerator.openDoor()
    try FoodTruck.shared.refrigerator.closeDoor()
    #expect(FoodTruck.shared.refrigerator.lightState == .off)
  }
}

```

For more information, see [Running tests serially or in parallel](https://developer.apple.com/documentation/testing/parallelization).

## [See Also](https://developer.apple.com/documentation/testing/migratingfromxctest\#see-also)

### [Related Documentation](https://developer.apple.com/documentation/testing/migratingfromxctest\#Related-Documentation)

[Defining test functions](https://developer.apple.com/documentation/testing/definingtests)

Define a test function to validate that code is working correctly.

[Organizing test functions with suite types](https://developer.apple.com/documentation/testing/organizingtests)

Organize tests into test suites.

[API Reference\\
Expectations and confirmations](https://developer.apple.com/documentation/testing/expectations)

Check for expected values, outcomes, and asynchronous events in tests.

[API Reference\\
Known issues](https://developer.apple.com/documentation/testing/known-issues)

Highlight known issues when running tests.

### [Essentials](https://developer.apple.com/documentation/testing/migratingfromxctest\#Essentials)

[Defining test functions](https://developer.apple.com/documentation/testing/definingtests)

Define a test function to validate that code is working correctly.

[Organizing test functions with suite types](https://developer.apple.com/documentation/testing/organizingtests)

Organize tests into test suites.

[`macro Test(String?, any TestTrait...)`](https://developer.apple.com/documentation/testing/test(_:_:))

Declare a test.

[`struct Test`](https://developer.apple.com/documentation/testing/test)

A type representing a test or suite.

[`macro Suite(String?, any SuiteTrait...)`](https://developer.apple.com/documentation/testing/suite(_:_:))

Declare a test suite.

Current page is Migrating a test from XCTest

## TestTrait Protocol
[Skip Navigation](https://developer.apple.com/documentation/testing/testtrait#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- TestTrait

Protocol

# TestTrait

A protocol describing a trait that you can add to a test function.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
protocol TestTrait : Trait
```

## [Overview](https://developer.apple.com/documentation/testing/testtrait\#overview)

The testing library defines a number of traits that you can add to test functions. You can also define your own traits by creating types that conform to this protocol, or to the [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait) protocol.

## [Relationships](https://developer.apple.com/documentation/testing/testtrait\#relationships)

### [Inherits From](https://developer.apple.com/documentation/testing/testtrait\#inherits-from)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)
- [`Trait`](https://developer.apple.com/documentation/testing/trait)

### [Conforming Types](https://developer.apple.com/documentation/testing/testtrait\#conforming-types)

- [`Bug`](https://developer.apple.com/documentation/testing/bug)
- [`Comment`](https://developer.apple.com/documentation/testing/comment)
- [`ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait)
- [`ParallelizationTrait`](https://developer.apple.com/documentation/testing/parallelizationtrait)
- [`Tag.List`](https://developer.apple.com/documentation/testing/tag/list)
- [`TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait)

## [See Also](https://developer.apple.com/documentation/testing/testtrait\#see-also)

### [Creating custom traits](https://developer.apple.com/documentation/testing/testtrait\#Creating-custom-traits)

[`protocol Trait`](https://developer.apple.com/documentation/testing/trait)

A protocol describing traits that can be added to a test function or to a test suite.

[`protocol SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait)

A protocol describing a trait that you can add to a test suite.

[`protocol TestScoping`](https://developer.apple.com/documentation/testing/testscoping)

A protocol that tells the test runner to run custom code before or after it runs a test suite or test function.

Current page is TestTrait

## Parallelization Trait
[Skip Navigation](https://developer.apple.com/documentation/testing/parallelizationtrait#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- ParallelizationTrait

Structure

# ParallelizationTrait

A type that defines whether the testing library runs this test serially or in parallel.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct ParallelizationTrait
```

## [Overview](https://developer.apple.com/documentation/testing/parallelizationtrait\#overview)

When you add this trait to a parameterized test function, that test runs its cases serially instead of in parallel. This trait has no effect when you apply it to a non-parameterized test function.

When you add this trait to a test suite, that suite runs its contained test functions (including their cases, when parameterized) and sub-suites serially instead of in parallel. If the sub-suites have children, they also run serially.

This trait does not affect the execution of a test relative to its peers or to unrelated tests. This trait has no effect if you disable test parallelization globally (for example, by passing `--no-parallel` to the `swift test` command.)

To add this trait to a test, use [`serialized`](https://developer.apple.com/documentation/testing/trait/serialized).

## [Topics](https://developer.apple.com/documentation/testing/parallelizationtrait\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/parallelizationtrait\#Instance-Properties)

[`var isRecursive: Bool`](https://developer.apple.com/documentation/testing/parallelizationtrait/isrecursive)

Whether this instance should be applied recursively to child test suites and test functions.

### [Type Aliases](https://developer.apple.com/documentation/testing/parallelizationtrait\#Type-Aliases)

[`typealias TestScopeProvider`](https://developer.apple.com/documentation/testing/parallelizationtrait/testscopeprovider)

The type of the test scope provider for this trait.

### [Default Implementations](https://developer.apple.com/documentation/testing/parallelizationtrait\#Default-Implementations)

[API Reference\\
Trait Implementations](https://developer.apple.com/documentation/testing/parallelizationtrait/trait-implementations)

## [Relationships](https://developer.apple.com/documentation/testing/parallelizationtrait\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/parallelizationtrait\#conforms-to)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)
- [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait)
- [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait)
- [`Trait`](https://developer.apple.com/documentation/testing/trait)

## [See Also](https://developer.apple.com/documentation/testing/parallelizationtrait\#see-also)

### [Supporting types](https://developer.apple.com/documentation/testing/parallelizationtrait\#Supporting-types)

[`struct Bug`](https://developer.apple.com/documentation/testing/bug)

A type that represents a bug report tracked by a test.

[`struct Comment`](https://developer.apple.com/documentation/testing/comment)

A type that represents a comment related to a test.

[`struct ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait)

A type that defines a condition which must be satisfied for the testing library to enable a test.

[`struct Tag`](https://developer.apple.com/documentation/testing/tag)

A type representing a tag that can be applied to a test.

[`struct List`](https://developer.apple.com/documentation/testing/tag/list)

A type representing one or more tags applied to a test.

[`struct TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait)

A type that defines a time limit to apply to a test.

Current page is ParallelizationTrait

## Test Execution Control
[Skip Navigation](https://developer.apple.com/documentation/testing/parallelization#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Traits](https://developer.apple.com/documentation/testing/traits)
- Running tests serially or in parallel

Article

# Running tests serially or in parallel

Control whether tests run serially or in parallel.

## [Overview](https://developer.apple.com/documentation/testing/parallelization\#Overview)

By default, tests run in parallel with respect to each other. Parallelization is accomplished by the testing library using task groups, and tests generally all run in the same process. The number of tests that run concurrently is controlled by the Swift runtime.

## [Disabling parallelization](https://developer.apple.com/documentation/testing/parallelization\#Disabling-parallelization)

Parallelization can be disabled on a per-function or per-suite basis using the [`serialized`](https://developer.apple.com/documentation/testing/trait/serialized) trait:

```
@Test(.serialized, arguments: Food.allCases) func prepare(food: Food) {
  // This function will be invoked serially, once per food, because it has the
  // .serialized trait.
}

@Suite(.serialized) struct FoodTruckTests {
  @Test(arguments: Condiment.allCases) func refill(condiment: Condiment) {
    // This function will be invoked serially, once per condiment, because the
    // containing suite has the .serialized trait.
  }

  @Test func startEngine() async throws {
    // This function will not run while refill(condiment:) is running. One test
    // must end before the other will start.
  }
}

```

When added to a parameterized test function, this trait causes that test to run its cases serially instead of in parallel. When applied to a non-parameterized test function, this trait has no effect. When applied to a test suite, this trait causes that suite to run its contained test functions and sub-suites serially instead of in parallel.

This trait is recursively applied: if it is applied to a suite, any parameterized tests or test suites contained in that suite are also serialized (as are any tests contained in those suites, and so on.)

This trait doesn’t affect the execution of a test relative to its peers or to unrelated tests. This trait has no effect if test parallelization is globally disabled (by, for example, passing `--no-parallel` to the `swift test` command.)

## [See Also](https://developer.apple.com/documentation/testing/parallelization\#see-also)

### [Running tests serially or in parallel](https://developer.apple.com/documentation/testing/parallelization\#Running-tests-serially-or-in-parallel)

[`static var serialized: ParallelizationTrait`](https://developer.apple.com/documentation/testing/trait/serialized)

A trait that serializes the test to which it is applied.

Current page is Running tests serially or in parallel

## Enabling Tests
[Skip Navigation](https://developer.apple.com/documentation/testing/enablinganddisabling#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Traits](https://developer.apple.com/documentation/testing/traits)
- Enabling and disabling tests

Article

# Enabling and disabling tests

Conditionally enable or disable individual tests before they run.

## [Overview](https://developer.apple.com/documentation/testing/enablinganddisabling\#Overview)

Often, a test is only applicable in specific circumstances. For instance, you might want to write a test that only runs on devices with particular hardware capabilities, or performs locale-dependent operations. The testing library allows you to add traits to your tests that cause runners to automatically skip them if conditions like these are not met.

### [Disable a test](https://developer.apple.com/documentation/testing/enablinganddisabling\#Disable-a-test)

If you need to disable a test unconditionally, use the [`disabled(_:sourceLocation:)`](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:)) function. Given the following test function:

```
@Test("Food truck sells burritos")
func sellsBurritos() async throws { ... }

```

Add the trait _after_ the test’s display name:

```
@Test("Food truck sells burritos", .disabled())
func sellsBurritos() async throws { ... }

```

The test will now always be skipped.

It’s also possible to add a comment to the trait to present in the output from the runner when it skips the test:

```
@Test("Food truck sells burritos", .disabled("We only sell Thai cuisine"))
func sellsBurritos() async throws { ... }

```

### [Enable or disable a test conditionally](https://developer.apple.com/documentation/testing/enablinganddisabling\#Enable-or-disable-a-test-conditionally)

Sometimes, it makes sense to enable a test only when a certain condition is met. Consider the following test function:

```
@Test("Ice cream is cold")
func isCold() async throws { ... }

```

If it’s currently winter, then presumably ice cream won’t be available for sale and this test will fail. It therefore makes sense to only enable it if it’s currently summer. You can conditionally enable a test with [`enabled(if:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/trait/enabled(if:_:sourcelocation:)):

```
@Test("Ice cream is cold", .enabled(if: Season.current == .summer))
func isCold() async throws { ... }

```

It’s also possible to conditionally _disable_ a test and to combine multiple conditions:

```
@Test(
  "Ice cream is cold",
  .enabled(if: Season.current == .summer),
  .disabled("We ran out of sprinkles")
)
func isCold() async throws { ... }

```

If a test is disabled because of a problem for which there is a corresponding bug report, you can use one of these functions to show the relationship between the test and the bug report:

- [`bug(_:_:)`](https://developer.apple.com/documentation/testing/trait/bug(_:_:))

- [`bug(_:id:_:)`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-10yf5)

- [`bug(_:id:_:)`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-3vtpl)


For example, the following test cannot run due to bug number `"12345"`:

```
@Test(
  "Ice cream is cold",
  .enabled(if: Season.current == .summer),
  .disabled("We ran out of sprinkles"),
  .bug(id: "12345")
)
func isCold() async throws { ... }

```

If a test has multiple conditions applied to it, they must _all_ pass for it to run. Otherwise, the test notes the first condition to fail as the reason the test is skipped.

### [Handle complex conditions](https://developer.apple.com/documentation/testing/enablinganddisabling\#Handle-complex-conditions)

If a condition is complex, consider factoring it out into a helper function to improve readability:

```
func allIngredientsAvailable(for food: Food) -> Bool { ... }

@Test(
  "Can make sundaes",
  .enabled(if: Season.current == .summer),
  .enabled(if: allIngredientsAvailable(for: .sundae))
)
func makeSundae() async throws { ... }

```

## [See Also](https://developer.apple.com/documentation/testing/enablinganddisabling\#see-also)

### [Customizing runtime behaviors](https://developer.apple.com/documentation/testing/enablinganddisabling\#Customizing-runtime-behaviors)

[Limiting the running time of tests](https://developer.apple.com/documentation/testing/limitingexecutiontime)

Set limits on how long a test can run for until it fails.

[`static func enabled(if: @autoclosure () throws -> Bool, Comment?, sourceLocation: SourceLocation) -> Self`](https://developer.apple.com/documentation/testing/trait/enabled(if:_:sourcelocation:))

Constructs a condition trait that disables a test if it returns `false`.

[`static func enabled(Comment?, sourceLocation: SourceLocation, () async throws -> Bool) -> Self`](https://developer.apple.com/documentation/testing/trait/enabled(_:sourcelocation:_:))

Constructs a condition trait that disables a test if it returns `false`.

[`static func disabled(Comment?, sourceLocation: SourceLocation) -> Self`](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:))

Constructs a condition trait that disables a test unconditionally.

[`static func disabled(if: @autoclosure () throws -> Bool, Comment?, sourceLocation: SourceLocation) -> Self`](https://developer.apple.com/documentation/testing/trait/disabled(if:_:sourcelocation:))

Constructs a condition trait that disables a test if its value is true.

[`static func disabled(Comment?, sourceLocation: SourceLocation, () async throws -> Bool) -> Self`](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:_:))

Constructs a condition trait that disables a test if its value is true.

[`static func timeLimit(TimeLimitTrait.Duration) -> Self`](https://developer.apple.com/documentation/testing/trait/timelimit(_:))

Construct a time limit trait that causes a test to time out if it runs for too long.

Current page is Enabling and disabling tests

## Testing Expectations
[Skip Navigation](https://developer.apple.com/documentation/testing/expectations#app-main)

Collection

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Expectations and confirmations

API Collection

# Expectations and confirmations

Check for expected values, outcomes, and asynchronous events in tests.

## [Overview](https://developer.apple.com/documentation/testing/expectations\#Overview)

Use [`expect(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:)) and [`require(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q) macros to validate expected outcomes. To validate that an error is thrown, or _not_ thrown, the testing library provides several overloads of the macros that you can use. For more information, see [Testing for errors in Swift code](https://developer.apple.com/documentation/testing/testing-for-errors-in-swift-code).

Use a [`Confirmation`](https://developer.apple.com/documentation/testing/confirmation) to confirm the occurrence of an asynchronous event that you can’t check directly using an expectation. For more information, see [Testing asynchronous code](https://developer.apple.com/documentation/testing/testing-asynchronous-code).

### [Validate your code’s result](https://developer.apple.com/documentation/testing/expectations\#Validate-your-codes-result)

To validate that your code produces an expected value, use [`expect(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:)). This macro captures the expression you pass, and provides detailed information when the code doesn’t satisfy the expectation.

```
@Test func calculatingOrderTotal() {
  let calculator = OrderCalculator()
  #expect(calculator.total(of: [3, 3]) == 7)
  // Prints "Expectation failed: (calculator.total(of: [3, 3]) → 6) == 7"
}

```

Your test keeps running after [`expect(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:)) fails. To stop the test when the code doesn’t satisfy a requirement, use [`require(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q) instead:

```
@Test func returningCustomerRemembersUsualOrder() throws {
  let customer = try #require(Customer(id: 123))
  // The test runner doesn't reach this line if the customer is nil.
  #expect(customer.usualOrder.countOfItems == 2)
}

```

[`require(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q) throws an instance of [`ExpectationFailedError`](https://developer.apple.com/documentation/testing/expectationfailederror) when your code fails to satisfy the requirement.

## [Topics](https://developer.apple.com/documentation/testing/expectations\#topics)

### [Checking expectations](https://developer.apple.com/documentation/testing/expectations\#Checking-expectations)

[`macro expect(Bool, @autoclosure () -> Comment?, sourceLocation: SourceLocation)`](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:))

Check that an expectation has passed after a condition has been evaluated.

[`macro require(Bool, @autoclosure () -> Comment?, sourceLocation: SourceLocation)`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q)

Check that an expectation has passed after a condition has been evaluated and throw an error if it failed.

[`macro require<T>(T?, @autoclosure () -> Comment?, sourceLocation: SourceLocation) -> T`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-6w9oo)

Unwrap an optional value or, if it is `nil`, fail and throw an error.

### [Checking that errors are thrown](https://developer.apple.com/documentation/testing/expectations\#Checking-that-errors-are-thrown)

[Testing for errors in Swift code](https://developer.apple.com/documentation/testing/testing-for-errors-in-swift-code)

Ensure that your code handles errors in the way you expect.

[`macro expect<E, R>(throws: E.Type, @autoclosure () -> Comment?, sourceLocation: SourceLocation, performing: () async throws -> R) -> E?`](https://developer.apple.com/documentation/testing/expect(throws:_:sourcelocation:performing:)-1hfms)

Check that an expression always throws an error of a given type.

[`macro expect<E, R>(throws: E, @autoclosure () -> Comment?, sourceLocation: SourceLocation, performing: () async throws -> R) -> E?`](https://developer.apple.com/documentation/testing/expect(throws:_:sourcelocation:performing:)-7du1h)

Check that an expression always throws a specific error.

[`macro expect<R>(@autoclosure () -> Comment?, sourceLocation: SourceLocation, performing: () async throws -> R, throws: (any Error) async throws -> Bool) -> (any Error)?`](https://developer.apple.com/documentation/testing/expect(_:sourcelocation:performing:throws:))

Check that an expression always throws an error matching some condition.

Deprecated

[`macro require<E, R>(throws: E.Type, @autoclosure () -> Comment?, sourceLocation: SourceLocation, performing: () async throws -> R) -> E`](https://developer.apple.com/documentation/testing/require(throws:_:sourcelocation:performing:)-7n34r)

Check that an expression always throws an error of a given type, and throw an error if it does not.

[`macro require<E, R>(throws: E, @autoclosure () -> Comment?, sourceLocation: SourceLocation, performing: () async throws -> R) -> E`](https://developer.apple.com/documentation/testing/require(throws:_:sourcelocation:performing:)-4djuw)

[`macro require<R>(@autoclosure () -> Comment?, sourceLocation: SourceLocation, performing: () async throws -> R, throws: (any Error) async throws -> Bool) -> any Error`](https://developer.apple.com/documentation/testing/require(_:sourcelocation:performing:throws:))

Check that an expression always throws an error matching some condition, and throw an error if it does not.

Deprecated

### [Confirming that asynchronous events occur](https://developer.apple.com/documentation/testing/expectations\#Confirming-that-asynchronous-events-occur)

[Testing asynchronous code](https://developer.apple.com/documentation/testing/testing-asynchronous-code)

Validate whether your code causes expected events to happen.

[`func confirmation<R>(Comment?, expectedCount: Int, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, (Confirmation) async throws -> sending R) async rethrows -> R`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-5mqz2)

Confirm that some event occurs during the invocation of a function.

[`func confirmation<R>(Comment?, expectedCount: some RangeExpression<Int> & Sendable & Sequence<Int>, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, (Confirmation) async throws -> sending R) async rethrows -> R`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-l3il)

Confirm that some event occurs during the invocation of a function.

[`struct Confirmation`](https://developer.apple.com/documentation/testing/confirmation)

A type that can be used to confirm that an event occurs zero or more times.

### [Retrieving information about checked expectations](https://developer.apple.com/documentation/testing/expectations\#Retrieving-information-about-checked-expectations)

[`struct Expectation`](https://developer.apple.com/documentation/testing/expectation)

A type describing an expectation that has been evaluated.

[`struct ExpectationFailedError`](https://developer.apple.com/documentation/testing/expectationfailederror)

A type describing an error thrown when an expectation fails during evaluation.

[`protocol CustomTestStringConvertible`](https://developer.apple.com/documentation/testing/customteststringconvertible)

A protocol describing types with a custom string representation when presented as part of a test’s output.

### [Representing source locations](https://developer.apple.com/documentation/testing/expectations\#Representing-source-locations)

[`struct SourceLocation`](https://developer.apple.com/documentation/testing/sourcelocation)

A type representing a location in source code.

## [See Also](https://developer.apple.com/documentation/testing/expectations\#see-also)

### [Behavior validation](https://developer.apple.com/documentation/testing/expectations\#Behavior-validation)

[API Reference\\
Known issues](https://developer.apple.com/documentation/testing/known-issues)

Highlight known issues when running tests.

Current page is Expectations and confirmations

## Known Issue Matcher
[Skip Navigation](https://developer.apple.com/documentation/testing/knownissuematcher#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- KnownIssueMatcher

Type Alias

# KnownIssueMatcher

A function that is used to match known issues.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
typealias KnownIssueMatcher = (Issue) -> Bool
```

## [Parameters](https://developer.apple.com/documentation/testing/knownissuematcher\#parameters)

`issue`

The issue to match.

## [Return Value](https://developer.apple.com/documentation/testing/knownissuematcher\#return-value)

Whether or not `issue` is known to occur.

## [See Also](https://developer.apple.com/documentation/testing/knownissuematcher\#see-also)

### [Recording known issues in tests](https://developer.apple.com/documentation/testing/knownissuematcher\#Recording-known-issues-in-tests)

[`func withKnownIssue(Comment?, isIntermittent: Bool, sourceLocation: SourceLocation, () throws -> Void)`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:))

Invoke a function that has a known issue that is expected to occur during its execution.

[`func withKnownIssue(Comment?, isIntermittent: Bool, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, () async throws -> Void) async`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:isolation:sourcelocation:_:))

Invoke a function that has a known issue that is expected to occur during its execution.

[`func withKnownIssue(Comment?, isIntermittent: Bool, sourceLocation: SourceLocation, () throws -> Void, when: () -> Bool, matching: KnownIssueMatcher) rethrows`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:when:matching:))

Invoke a function that has a known issue that is expected to occur during its execution.

[`func withKnownIssue(Comment?, isIntermittent: Bool, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, () async throws -> Void, when: () async -> Bool, matching: KnownIssueMatcher) async rethrows`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:isolation:sourcelocation:_:when:matching:))

Invoke a function that has a known issue that is expected to occur during its execution.

Current page is KnownIssueMatcher

## Associating Bugs with Tests
[Skip Navigation](https://developer.apple.com/documentation/testing/associatingbugs#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Traits](https://developer.apple.com/documentation/testing/traits)
- Associating bugs with tests

Article

# Associating bugs with tests

Associate bugs uncovered or verified by tests.

## [Overview](https://developer.apple.com/documentation/testing/associatingbugs\#Overview)

Tests allow developers to prove that the code they write is working as expected. If code isn’t working correctly, bug trackers are often used to track the work necessary to fix the underlying problem. It’s often useful to associate specific bugs with tests that reproduce them or verify they are fixed.

## [Associate a bug with a test](https://developer.apple.com/documentation/testing/associatingbugs\#Associate-a-bug-with-a-test)

To associate a bug with a test, use one of these functions:

- [`bug(_:_:)`](https://developer.apple.com/documentation/testing/trait/bug(_:_:))

- [`bug(_:id:_:)`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-10yf5)

- [`bug(_:id:_:)`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-3vtpl)


The first argument to these functions is a URL representing the bug in its bug-tracking system:

```
@Test("Food truck engine works", .bug("https://www.example.com/issues/12345"))
func engineWorks() async {
  var foodTruck = FoodTruck()
  await foodTruck.engine.start()
  #expect(foodTruck.engine.isRunning)
}

```

You can also specify the bug’s _unique identifier_ in its bug-tracking system in addition to, or instead of, its URL:

```
@Test(
  "Food truck engine works",
  .bug(id: "12345"),
  .bug("https://www.example.com/issues/67890", id: 67890)
)
func engineWorks() async {
  var foodTruck = FoodTruck()
  await foodTruck.engine.start()
  #expect(foodTruck.engine.isRunning)
}

```

A bug’s URL is passed as a string and must be parseable according to [RFC 3986](https://www.ietf.org/rfc/rfc3986.txt). A bug’s unique identifier can be passed as an integer or as a string. For more information on the formats recognized by the testing library, see [Interpreting bug identifiers](https://developer.apple.com/documentation/testing/bugidentifiers).

## [Add titles to associated bugs](https://developer.apple.com/documentation/testing/associatingbugs\#Add-titles-to-associated-bugs)

A bug’s unique identifier or URL may be insufficient to uniquely and clearly identify a bug associated with a test. Bug trackers universally provide a “title” field for bugs that is not visible to the testing library. To add a bug’s title to a test, include it after the bug’s unique identifier or URL:

```
@Test(
  "Food truck has napkins",
  .bug(id: "12345", "Forgot to buy more napkins")
)
func hasNapkins() async {
  ...
}

```

## [See Also](https://developer.apple.com/documentation/testing/associatingbugs\#see-also)

### [Annotating tests](https://developer.apple.com/documentation/testing/associatingbugs\#Annotating-tests)

[Adding tags to tests](https://developer.apple.com/documentation/testing/addingtags)

Use tags to provide semantic information for organization, filtering, and customizing appearances.

[Adding comments to tests](https://developer.apple.com/documentation/testing/addingcomments)

Add comments to provide useful information about tests.

[Interpreting bug identifiers](https://developer.apple.com/documentation/testing/bugidentifiers)

Examine how the testing library interprets bug identifiers provided by developers.

[`macro Tag()`](https://developer.apple.com/documentation/testing/tag())

Declare a tag that can be applied to a test function or test suite.

[`static func bug(String, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:_:))

Constructs a bug to track with a test.

[`static func bug(String?, id: String, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-10yf5)

Constructs a bug to track with a test.

[`static func bug(String?, id: some Numeric, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-3vtpl)

Constructs a bug to track with a test.

Current page is Associating bugs with tests

## Test Comment Structure
[Skip Navigation](https://developer.apple.com/documentation/testing/comment#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Comment

Structure

# Comment

A type that represents a comment related to a test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct Comment
```

## [Overview](https://developer.apple.com/documentation/testing/comment\#overview)

Use this type to provide context or background information about a test’s purpose, explain how a complex test operates, or include details which may be helpful when diagnosing issues recorded by a test.

To add a comment to a test or suite, add a code comment before its `@Test` or `@Suite` attribute. See [Adding comments to tests](https://developer.apple.com/documentation/testing/addingcomments) for more details.

## [Topics](https://developer.apple.com/documentation/testing/comment\#topics)

### [Initializers](https://developer.apple.com/documentation/testing/comment\#Initializers)

[`init(rawValue: String)`](https://developer.apple.com/documentation/testing/comment/init(rawvalue:))

Creates a new instance with the specified raw value.

### [Instance Properties](https://developer.apple.com/documentation/testing/comment\#Instance-Properties)

[`var rawValue: String`](https://developer.apple.com/documentation/testing/comment/rawvalue-swift.property)

The single comment string that this comment contains.

### [Type Aliases](https://developer.apple.com/documentation/testing/comment\#Type-Aliases)

[`typealias RawValue`](https://developer.apple.com/documentation/testing/comment/rawvalue-swift.typealias)

The raw type that can be used to represent all values of the conforming type.

### [Default Implementations](https://developer.apple.com/documentation/testing/comment\#Default-Implementations)

[API Reference\\
CustomStringConvertible Implementations](https://developer.apple.com/documentation/testing/comment/customstringconvertible-implementations)

[API Reference\\
Equatable Implementations](https://developer.apple.com/documentation/testing/comment/equatable-implementations)

[API Reference\\
ExpressibleByExtendedGraphemeClusterLiteral Implementations](https://developer.apple.com/documentation/testing/comment/expressiblebyextendedgraphemeclusterliteral-implementations)

[API Reference\\
ExpressibleByStringInterpolation Implementations](https://developer.apple.com/documentation/testing/comment/expressiblebystringinterpolation-implementations)

[API Reference\\
ExpressibleByStringLiteral Implementations](https://developer.apple.com/documentation/testing/comment/expressiblebystringliteral-implementations)

[API Reference\\
ExpressibleByUnicodeScalarLiteral Implementations](https://developer.apple.com/documentation/testing/comment/expressiblebyunicodescalarliteral-implementations)

[API Reference\\
RawRepresentable Implementations](https://developer.apple.com/documentation/testing/comment/rawrepresentable-implementations)

[API Reference\\
SuiteTrait Implementations](https://developer.apple.com/documentation/testing/comment/suitetrait-implementations)

[API Reference\\
Trait Implementations](https://developer.apple.com/documentation/testing/comment/trait-implementations)

## [Relationships](https://developer.apple.com/documentation/testing/comment\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/comment\#conforms-to)

- [`Copyable`](https://developer.apple.com/documentation/Swift/Copyable)
- [`CustomStringConvertible`](https://developer.apple.com/documentation/Swift/CustomStringConvertible)
- [`Decodable`](https://developer.apple.com/documentation/Swift/Decodable)
- [`Encodable`](https://developer.apple.com/documentation/Swift/Encodable)
- [`Equatable`](https://developer.apple.com/documentation/Swift/Equatable)
- [`ExpressibleByExtendedGraphemeClusterLiteral`](https://developer.apple.com/documentation/Swift/ExpressibleByExtendedGraphemeClusterLiteral)
- [`ExpressibleByStringInterpolation`](https://developer.apple.com/documentation/Swift/ExpressibleByStringInterpolation)
- [`ExpressibleByStringLiteral`](https://developer.apple.com/documentation/Swift/ExpressibleByStringLiteral)
- [`ExpressibleByUnicodeScalarLiteral`](https://developer.apple.com/documentation/Swift/ExpressibleByUnicodeScalarLiteral)
- [`Hashable`](https://developer.apple.com/documentation/Swift/Hashable)
- [`RawRepresentable`](https://developer.apple.com/documentation/Swift/RawRepresentable)
- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)
- [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait)
- [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait)
- [`Trait`](https://developer.apple.com/documentation/testing/trait)

## [See Also](https://developer.apple.com/documentation/testing/comment\#see-also)

### [Supporting types](https://developer.apple.com/documentation/testing/comment\#Supporting-types)

[`struct Bug`](https://developer.apple.com/documentation/testing/bug)

A type that represents a bug report tracked by a test.

[`struct ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait)

A type that defines a condition which must be satisfied for the testing library to enable a test.

[`struct ParallelizationTrait`](https://developer.apple.com/documentation/testing/parallelizationtrait)

A type that defines whether the testing library runs this test serially or in parallel.

[`struct Tag`](https://developer.apple.com/documentation/testing/tag)

A type representing a tag that can be applied to a test.

[`struct List`](https://developer.apple.com/documentation/testing/tag/list)

A type representing one or more tags applied to a test.

[`struct TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait)

A type that defines a time limit to apply to a test.

Current page is Comment

## Swift Test Time Limit
[Skip Navigation](https://developer.apple.com/documentation/testing/test/timelimit#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Test](https://developer.apple.com/documentation/testing/test)
- timeLimit

Instance Property

# timeLimit

The maximum amount of time this test’s cases may run for.

iOS 16.0+iPadOS 16.0+Mac Catalyst 16.0+macOS 13.0+tvOS 16.0+visionOSwatchOS 9.0+Swift 6.0+Xcode 16.0+

```
var timeLimit: Duration? { get }
```

## [Discussion](https://developer.apple.com/documentation/testing/test/timelimit\#discussion)

Associate a time limit with tests by using [`timeLimit(_:)`](https://developer.apple.com/documentation/testing/trait/timelimit(_:)).

If a test has more than one time limit associated with it, the value of this property is the shortest one. If a test has no time limits associated with it, the value of this property is `nil`.

Current page is timeLimit

## Swift fileID Property
[Skip Navigation](https://developer.apple.com/documentation/testing/sourcelocation/fileid#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [SourceLocation](https://developer.apple.com/documentation/testing/sourcelocation)
- fileID

Instance Property

# fileID

The file ID of the source file.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var fileID: String { get set }
```

## [Discussion](https://developer.apple.com/documentation/testing/sourcelocation/fileid\#discussion)

## [See Also](https://developer.apple.com/documentation/testing/sourcelocation/fileid\#see-also)

### [Related Documentation](https://developer.apple.com/documentation/testing/sourcelocation/fileid\#Related-Documentation)

[`var moduleName: String`](https://developer.apple.com/documentation/testing/sourcelocation/modulename)

The name of the module containing the source file.

[`var fileName: String`](https://developer.apple.com/documentation/testing/sourcelocation/filename)

The name of the source file.

Current page is fileID

## Tag() Macro
[Skip Navigation](https://developer.apple.com/documentation/testing/tag()#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Tag()

Macro

# Tag()

Declare a tag that can be applied to a test function or test suite.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
@attached(accessor) @attached(peer)
macro Tag()
```

## [Mentioned in](https://developer.apple.com/documentation/testing/tag()\#mentions)

[Adding tags to tests](https://developer.apple.com/documentation/testing/addingtags)

## [Overview](https://developer.apple.com/documentation/testing/tag()\#overview)

Use this tag with members of the [`Tag`](https://developer.apple.com/documentation/testing/tag) type declared in an extension to mark them as usable with tests. For more information on declaring tags, see [Adding tags to tests](https://developer.apple.com/documentation/testing/addingtags).

## [See Also](https://developer.apple.com/documentation/testing/tag()\#see-also)

### [Annotating tests](https://developer.apple.com/documentation/testing/tag()\#Annotating-tests)

[Adding tags to tests](https://developer.apple.com/documentation/testing/addingtags)

Use tags to provide semantic information for organization, filtering, and customizing appearances.

[Adding comments to tests](https://developer.apple.com/documentation/testing/addingcomments)

Add comments to provide useful information about tests.

[Associating bugs with tests](https://developer.apple.com/documentation/testing/associatingbugs)

Associate bugs uncovered or verified by tests.

[Interpreting bug identifiers](https://developer.apple.com/documentation/testing/bugidentifiers)

Examine how the testing library interprets bug identifiers provided by developers.

[`static func bug(String, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:_:))

Constructs a bug to track with a test.

[`static func bug(String?, id: String, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-10yf5)

Constructs a bug to track with a test.

[`static func bug(String?, id: some Numeric, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-3vtpl)

Constructs a bug to track with a test.

Current page is Tag()

## Swift Testing Error
[Skip Navigation](https://developer.apple.com/documentation/testing/issue/error#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Issue](https://developer.apple.com/documentation/testing/issue)
- error

Instance Property

# error

The error which was associated with this issue, if any.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var error: (any Error)? { get }
```

## [Discussion](https://developer.apple.com/documentation/testing/issue/error\#discussion)

The value of this property is non- `nil` when [`kind`](https://developer.apple.com/documentation/testing/issue/kind-swift.property) is [`Issue.Kind.errorCaught(_:)`](https://developer.apple.com/documentation/testing/issue/kind-swift.enum/errorcaught(_:)).

Current page is error

## Test Description Property
[Skip Navigation](https://developer.apple.com/documentation/testing/customteststringconvertible/testdescription#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [CustomTestStringConvertible](https://developer.apple.com/documentation/testing/customteststringconvertible)
- testDescription

Instance Property

# testDescription

A description of this instance to use when presenting it in a test’s output.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var testDescription: String { get }
```

**Required** Default implementation provided.

## [Discussion](https://developer.apple.com/documentation/testing/customteststringconvertible/testdescription\#discussion)

Do not use this property directly. To get the test description of a value, use `Swift/String/init(describingForTest:)`.

## [Default Implementations](https://developer.apple.com/documentation/testing/customteststringconvertible/testdescription\#default-implementations)

### [CustomTestStringConvertible Implementations](https://developer.apple.com/documentation/testing/customteststringconvertible/testdescription\#CustomTestStringConvertible-Implementations)

[`var testDescription: String`](https://developer.apple.com/documentation/testing/customteststringconvertible/testdescription-3ar66)

A description of this instance to use when presenting it in a test’s output.

Current page is testDescription

## Source Location Trait
[Skip Navigation](https://developer.apple.com/documentation/testing/conditiontrait/sourcelocation#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [ConditionTrait](https://developer.apple.com/documentation/testing/conditiontrait)
- sourceLocation

Instance Property

# sourceLocation

The source location where this trait is specified.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var sourceLocation: SourceLocation
```

Current page is sourceLocation

## Swift Testing Name Property
[Skip Navigation](https://developer.apple.com/documentation/testing/test/name#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Test](https://developer.apple.com/documentation/testing/test)
- name

Instance Property

# name

The name of this instance.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var name: String
```

## [Discussion](https://developer.apple.com/documentation/testing/test/name\#discussion)

The value of this property is equal to the name of the symbol to which the [`Test`](https://developer.apple.com/documentation/testing/test) attribute is applied (that is, the name of the type or function.) To get the customized display name specified as part of the [`Test`](https://developer.apple.com/documentation/testing/test) attribute, use the [`displayName`](https://developer.apple.com/documentation/testing/test/displayname) property.

Current page is name

## isRecursive Trait
[Skip Navigation](https://developer.apple.com/documentation/testing/suitetrait/isrecursive#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [SuiteTrait](https://developer.apple.com/documentation/testing/suitetrait)
- isRecursive

Instance Property

# isRecursive

Whether this instance should be applied recursively to child test suites and test functions.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var isRecursive: Bool { get }
```

**Required** Default implementation provided.

## [Discussion](https://developer.apple.com/documentation/testing/suitetrait/isrecursive\#discussion)

If the value is `true`, then the testing library applies this trait recursively to child test suites and test functions. Otherwise, it only applies the trait to the test suite to which you added the trait.

By default, traits are not recursively applied to children.

## [Default Implementations](https://developer.apple.com/documentation/testing/suitetrait/isrecursive\#default-implementations)

### [SuiteTrait Implementations](https://developer.apple.com/documentation/testing/suitetrait/isrecursive\#SuiteTrait-Implementations)

[`var isRecursive: Bool`](https://developer.apple.com/documentation/testing/suitetrait/isrecursive-2z41z)

Whether this instance should be applied recursively to child test suites and test functions.

Current page is isRecursive

## Swift fileName Property
[Skip Navigation](https://developer.apple.com/documentation/testing/sourcelocation/filename#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [SourceLocation](https://developer.apple.com/documentation/testing/sourcelocation)
- fileName

Instance Property

# fileName

The name of the source file.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var fileName: String { get }
```

## [Discussion](https://developer.apple.com/documentation/testing/sourcelocation/filename\#discussion)

The name of the source file is derived from this instance’s [`fileID`](https://developer.apple.com/documentation/testing/sourcelocation/fileid) property. It consists of the substring of the file ID after the last forward-slash character ( `"/"`.) For example, if the value of this instance’s [`fileID`](https://developer.apple.com/documentation/testing/sourcelocation/fileid) property is `"FoodTruck/WheelTests.swift"`, the file name is `"WheelTests.swift"`.

The structure of file IDs is described in the documentation for [`#fileID`](https://developer.apple.com/documentation/swift/fileID()) in the Swift standard library.

## [See Also](https://developer.apple.com/documentation/testing/sourcelocation/filename\#see-also)

### [Related Documentation](https://developer.apple.com/documentation/testing/sourcelocation/filename\#Related-Documentation)

[`var fileID: String`](https://developer.apple.com/documentation/testing/sourcelocation/fileid)

The file ID of the source file.

[`var moduleName: String`](https://developer.apple.com/documentation/testing/sourcelocation/modulename)

The name of the module containing the source file.

Current page is fileName

## Developer Comments Management
[Skip Navigation](https://developer.apple.com/documentation/testing/issue/comments#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Issue](https://developer.apple.com/documentation/testing/issue)
- comments

Instance Property

# comments

Any comments provided by the developer and associated with this issue.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var comments: [Comment]
```

## [Discussion](https://developer.apple.com/documentation/testing/issue/comments\#discussion)

If no comment was supplied when the issue occurred, the value of this property is the empty array.

Current page is comments

## Source Location in Testing
[Skip Navigation](https://developer.apple.com/documentation/testing/issue/sourcelocation#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Issue](https://developer.apple.com/documentation/testing/issue)
- sourceLocation

Instance Property

# sourceLocation

The location in source where this issue occurred, if available.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var sourceLocation: SourceLocation? { get set }
```

Current page is sourceLocation

## Test Comments
[Skip Navigation](https://developer.apple.com/documentation/testing/test/comments#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Test](https://developer.apple.com/documentation/testing/test)
- comments

Instance Property

# comments

The complete set of comments about this test from all of its traits.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var comments: [Comment] { get }
```

Current page is comments

## Test Duration Type
[Skip Navigation](https://developer.apple.com/documentation/testing/timelimittrait/duration#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [TimeLimitTrait](https://developer.apple.com/documentation/testing/timelimittrait)
- TimeLimitTrait.Duration

Structure

# TimeLimitTrait.Duration

A type representing the duration of a time limit applied to a test.

iOS 16.0+iPadOS 16.0+Mac Catalyst 16.0+macOS 13.0+tvOS 16.0+visionOSwatchOS 9.0+Swift 6.0+Xcode 16.0+

```
struct Duration
```

## [Overview](https://developer.apple.com/documentation/testing/timelimittrait/duration\#overview)

Use this type to specify a test timeout with [`TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait). `TimeLimitTrait` uses this type instead of Swift’s built-in `Duration` type because the testing library doesn’t support high-precision, arbitrarily short durations for test timeouts. The smallest unit of time you can specify in a `Duration` is minutes.

## [Topics](https://developer.apple.com/documentation/testing/timelimittrait/duration\#topics)

### [Type Methods](https://developer.apple.com/documentation/testing/timelimittrait/duration\#Type-Methods)

[`static func minutes(some BinaryInteger) -> TimeLimitTrait.Duration`](https://developer.apple.com/documentation/testing/timelimittrait/duration/minutes(_:))

Construct a time limit duration given a number of minutes.

## [Relationships](https://developer.apple.com/documentation/testing/timelimittrait/duration\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/timelimittrait/duration\#conforms-to)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)

Current page is TimeLimitTrait.Duration

## Test Tags Overview
[Skip Navigation](https://developer.apple.com/documentation/testing/test/tags#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Test](https://developer.apple.com/documentation/testing/test)
- tags

Instance Property

# tags

The complete, unique set of tags associated with this test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var tags: Set<Tag> { get }
```

## [Discussion](https://developer.apple.com/documentation/testing/test/tags\#discussion)

Tags are associated with tests using the [`tags(_:)`](https://developer.apple.com/documentation/testing/trait/tags(_:)) function.

Current page is tags

## Customizing Display Names
[Skip Navigation](https://developer.apple.com/documentation/testing/test/displayname#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Test](https://developer.apple.com/documentation/testing/test)
- displayName

Instance Property

# displayName

The customized display name of this instance, if specified.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var displayName: String?
```

Current page is displayName

## Serialized Trait
[Skip Navigation](https://developer.apple.com/documentation/testing/trait/serialized#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Trait](https://developer.apple.com/documentation/testing/trait)
- serialized

Type Property

# serialized

A trait that serializes the test to which it is applied.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
static var serialized: ParallelizationTrait { get }
```

Available when `Self` is `ParallelizationTrait`.

## [Mentioned in](https://developer.apple.com/documentation/testing/trait/serialized\#mentions)

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

[Running tests serially or in parallel](https://developer.apple.com/documentation/testing/parallelization)

## [See Also](https://developer.apple.com/documentation/testing/trait/serialized\#see-also)

### [Related Documentation](https://developer.apple.com/documentation/testing/trait/serialized\#Related-Documentation)

[`struct ParallelizationTrait`](https://developer.apple.com/documentation/testing/parallelizationtrait)

A type that defines whether the testing library runs this test serially or in parallel.

### [Running tests serially or in parallel](https://developer.apple.com/documentation/testing/trait/serialized\#Running-tests-serially-or-in-parallel)

[Running tests serially or in parallel](https://developer.apple.com/documentation/testing/parallelization)

Control whether tests run serially or in parallel.

Current page is serialized

## Swift Test Source Location
[Skip Navigation](https://developer.apple.com/documentation/testing/test/sourcelocation#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Test](https://developer.apple.com/documentation/testing/test)
- sourceLocation

Instance Property

# sourceLocation

The source location of this test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var sourceLocation: SourceLocation
```

Current page is sourceLocation

## Test Case Overview
[Skip Navigation](https://developer.apple.com/documentation/testing/test/case#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Test](https://developer.apple.com/documentation/testing/test)
- Test.Case

Structure

# Test.Case

A single test case from a parameterized [`Test`](https://developer.apple.com/documentation/testing/test).

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct Case
```

## [Overview](https://developer.apple.com/documentation/testing/test/case\#overview)

A test case represents a test run with a particular combination of inputs. Tests that are _not_ parameterized map to a single instance of [`Test.Case`](https://developer.apple.com/documentation/testing/test/case).

## [Topics](https://developer.apple.com/documentation/testing/test/case\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/test/case\#Instance-Properties)

[`var isParameterized: Bool`](https://developer.apple.com/documentation/testing/test/case/isparameterized)

Whether or not this test case is from a parameterized test.

### [Type Properties](https://developer.apple.com/documentation/testing/test/case\#Type-Properties)

[`static var current: Test.Case?`](https://developer.apple.com/documentation/testing/test/case/current)

The test case that is running on the current task, if any.

## [Relationships](https://developer.apple.com/documentation/testing/test/case\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/test/case\#conforms-to)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)

## [See Also](https://developer.apple.com/documentation/testing/test/case\#see-also)

### [Test parameterization](https://developer.apple.com/documentation/testing/test/case\#Test-parameterization)

[Implementing parameterized tests](https://developer.apple.com/documentation/testing/parameterizedtesting)

Specify different input parameters to generate multiple test cases from a test function.

[`macro Test<C>(String?, any TestTrait..., arguments: C)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-8kn7a)

Declare a test parameterized over a collection of values.

[`macro Test<C1, C2>(String?, any TestTrait..., arguments: C1, C2)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:_:))

Declare a test parameterized over two collections of values.

[`macro Test<C1, C2>(String?, any TestTrait..., arguments: Zip2Sequence<C1, C2>)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok)

Declare a test parameterized over two zipped collections of values.

[`protocol CustomTestArgumentEncodable`](https://developer.apple.com/documentation/testing/customtestargumentencodable)

A protocol for customizing how arguments passed to parameterized tests are encoded, which is used to match against when running specific arguments.

Current page is Test.Case

## Tag List Overview
[Skip Navigation](https://developer.apple.com/documentation/testing/tag/list#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Tag](https://developer.apple.com/documentation/testing/tag)
- Tag.List

Structure

# Tag.List

A type representing one or more tags applied to a test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct List
```

## [Overview](https://developer.apple.com/documentation/testing/tag/list\#overview)

To add this trait to a test, use the [`tags(_:)`](https://developer.apple.com/documentation/testing/trait/tags(_:)) function.

## [Topics](https://developer.apple.com/documentation/testing/tag/list\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/tag/list\#Instance-Properties)

[`var tags: [Tag]`](https://developer.apple.com/documentation/testing/tag/list/tags)

The list of tags contained in this instance.

### [Default Implementations](https://developer.apple.com/documentation/testing/tag/list\#Default-Implementations)

[API Reference\\
CustomStringConvertible Implementations](https://developer.apple.com/documentation/testing/tag/list/customstringconvertible-implementations)

[API Reference\\
Equatable Implementations](https://developer.apple.com/documentation/testing/tag/list/equatable-implementations)

[API Reference\\
Hashable Implementations](https://developer.apple.com/documentation/testing/tag/list/hashable-implementations)

[API Reference\\
SuiteTrait Implementations](https://developer.apple.com/documentation/testing/tag/list/suitetrait-implementations)

[API Reference\\
Trait Implementations](https://developer.apple.com/documentation/testing/tag/list/trait-implementations)

## [Relationships](https://developer.apple.com/documentation/testing/tag/list\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/tag/list\#conforms-to)

- [`Copyable`](https://developer.apple.com/documentation/Swift/Copyable)
- [`CustomStringConvertible`](https://developer.apple.com/documentation/Swift/CustomStringConvertible)
- [`Equatable`](https://developer.apple.com/documentation/Swift/Equatable)
- [`Hashable`](https://developer.apple.com/documentation/Swift/Hashable)
- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)
- [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait)
- [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait)
- [`Trait`](https://developer.apple.com/documentation/testing/trait)

## [See Also](https://developer.apple.com/documentation/testing/tag/list\#see-also)

### [Supporting types](https://developer.apple.com/documentation/testing/tag/list\#Supporting-types)

[`struct Bug`](https://developer.apple.com/documentation/testing/bug)

A type that represents a bug report tracked by a test.

[`struct Comment`](https://developer.apple.com/documentation/testing/comment)

A type that represents a comment related to a test.

[`struct ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait)

A type that defines a condition which must be satisfied for the testing library to enable a test.

[`struct ParallelizationTrait`](https://developer.apple.com/documentation/testing/parallelizationtrait)

A type that defines whether the testing library runs this test serially or in parallel.

[`struct Tag`](https://developer.apple.com/documentation/testing/tag)

A type representing a tag that can be applied to a test.

[`struct TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait)

A type that defines a time limit to apply to a test.

Current page is Tag.List

## Test Suite Indicator
[Skip Navigation](https://developer.apple.com/documentation/testing/test/issuite#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Test](https://developer.apple.com/documentation/testing/test)
- isSuite

Instance Property

# isSuite

Whether or not this instance is a test suite containing other tests.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var isSuite: Bool { get }
```

## [Discussion](https://developer.apple.com/documentation/testing/test/issuite\#discussion)

Instances of [`Test`](https://developer.apple.com/documentation/testing/test) attached to types rather than functions are test suites. They do not contain any test logic of their own, but they may have traits added to them that also apply to their subtests.

A test suite can be declared using the [`Suite(_:_:)`](https://developer.apple.com/documentation/testing/suite(_:_:)) macro.

Current page is isSuite

## Swift moduleName Property
[Skip Navigation](https://developer.apple.com/documentation/testing/sourcelocation/modulename#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [SourceLocation](https://developer.apple.com/documentation/testing/sourcelocation)
- moduleName

Instance Property

# moduleName

The name of the module containing the source file.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var moduleName: String { get }
```

## [Discussion](https://developer.apple.com/documentation/testing/sourcelocation/modulename\#discussion)

The name of the module is derived from this instance’s [`fileID`](https://developer.apple.com/documentation/testing/sourcelocation/fileid) property. It consists of the substring of the file ID up to the first forward-slash character ( `"/"`.) For example, if the value of this instance’s [`fileID`](https://developer.apple.com/documentation/testing/sourcelocation/fileid) property is `"FoodTruck/WheelTests.swift"`, the module name is `"FoodTruck"`.

The structure of file IDs is described in the documentation for the [`#fileID`](https://developer.apple.com/documentation/swift/fileID()) macro in the Swift standard library.

## [See Also](https://developer.apple.com/documentation/testing/sourcelocation/modulename\#see-also)

### [Related Documentation](https://developer.apple.com/documentation/testing/sourcelocation/modulename\#Related-Documentation)

[`var fileID: String`](https://developer.apple.com/documentation/testing/sourcelocation/fileid)

The file ID of the source file.

[`var fileName: String`](https://developer.apple.com/documentation/testing/sourcelocation/filename)

The name of the source file.

[#fileID](https://developer.apple.com/documentation/swift/fileID())

Current page is moduleName

## Swift Testing Comments
[Skip Navigation](https://developer.apple.com/documentation/testing/comment/comments#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Comment](https://developer.apple.com/documentation/testing/comment)
- comments

Instance Property

# comments

