The user-provided comments for this trait.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var comments: [Comment] { get }
```

## [Discussion](https://developer.apple.com/documentation/testing/comment/comments\#discussion)

The default value of this property is an empty array.

Current page is comments

## Associated Bugs in Testing
[Skip Navigation](https://developer.apple.com/documentation/testing/test/associatedbugs#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Test](https://developer.apple.com/documentation/testing/test)
- associatedBugs

Instance Property

# associatedBugs

The set of bugs associated with this test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var associatedBugs: [Bug] { get }
```

## [Discussion](https://developer.apple.com/documentation/testing/test/associatedbugs\#discussion)

For information on how to associate a bug with a test, see the documentation for [`Bug`](https://developer.apple.com/documentation/testing/bug).

Current page is associatedBugs

## Expectation Requirement
[Skip Navigation](https://developer.apple.com/documentation/testing/expectation/isrequired#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Expectation](https://developer.apple.com/documentation/testing/expectation)
- isRequired

Instance Property

# isRequired

Whether or not the expectation was required to pass.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var isRequired: Bool
```

Current page is isRequired

## Testing Asynchronous Code
[Skip Navigation](https://developer.apple.com/documentation/testing/testing-asynchronous-code#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Expectations and confirmations](https://developer.apple.com/documentation/testing/expectations)
- Testing asynchronous code

Article

# Testing asynchronous code

Validate whether your code causes expected events to happen.

## [Overview](https://developer.apple.com/documentation/testing/testing-asynchronous-code\#Overview)

The testing library integrates with Swift concurrency, meaning that in many situations you can test asynchronous code using standard Swift features. Mark your test function as `async` and, in the function body, `await` any asynchronous interactions:

```
@Test func priceLookupYieldsExpectedValue() async {
  let mozarellaPrice = await unitPrice(for: .mozarella)
  #expect(mozarellaPrice == 3)
}

```

In more complex situations you can use [`Confirmation`](https://developer.apple.com/documentation/testing/confirmation) to discover whether an expected event happens.

### [Confirm that an event happens](https://developer.apple.com/documentation/testing/testing-asynchronous-code\#Confirm-that-an-event-happens)

Call [`confirmation(_:expectedCount:isolation:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-5mqz2) in your asynchronous test function to create a `Confirmation` for the expected event. In the trailing closure parameter, call the code under test. Swift Testing passes a `Confirmation` as the parameter to the closure, which you call as a function in the event handler for the code under test when the event you’re testing for occurs:

```
@Test("OrderCalculator successfully calculates subtotal for no pizzas")
func subtotalForNoPizzas() async {
  let calculator = OrderCalculator()
  await confirmation() { confirmation in
    calculator.successHandler = { _ in confirmation() }
    _ = await calculator.subtotal(for: PizzaToppings(bases: []))
  }
}

```

If you expect the event to happen more than once, set the `expectedCount` parameter to the number of expected occurrences. The test passes if the number of occurrences during the test matches the expected count, and fails otherwise.

You can also pass a range to [`confirmation(_:expectedCount:isolation:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-l3il) if the exact number of times the event occurs may change over time or is random:

```
@Test("Customers bought sandwiches")
func boughtSandwiches() async {
  await confirmation(expectedCount: 0 ..< 1000) { boughtSandwich in
    var foodTruck = FoodTruck()
    foodTruck.orderHandler = { order in
      if order.contains(.sandwich) {
        boughtSandwich()
      }
    }
    await FoodTruck.operate()
  }
}

```

In this example, there may be zero customers or up to (but not including) 1,000 customers who order sandwiches. Any [range expression](https://developer.apple.com/documentation/swift/rangeexpression) which includes an explicit lower bound can be used:

| Range Expression | Usage |
| --- | --- |
| `1...` | If an event must occur _at least_ once |
| `5...` | If an event must occur _at least_ five times |
| `1 ... 5` | If an event must occur at least once, but not more than five times |
| `0 ..< 100` | If an event may or may not occur, but _must not_ occur more than 99 times |

### [Confirm that an event doesn’t happen](https://developer.apple.com/documentation/testing/testing-asynchronous-code\#Confirm-that-an-event-doesnt-happen)

To validate that a particular event doesn’t occur during a test, create a `Confirmation` with an expected count of `0`:

```
@Test func orderCalculatorEncountersNoErrors() async {
  let calculator = OrderCalculator()
  await confirmation(expectedCount: 0) { confirmation in
    calculator.errorHandler = { _ in confirmation() }
    calculator.subtotal(for: PizzaToppings(bases: []))
  }
}

```

## [See Also](https://developer.apple.com/documentation/testing/testing-asynchronous-code\#see-also)

### [Confirming that asynchronous events occur](https://developer.apple.com/documentation/testing/testing-asynchronous-code\#Confirming-that-asynchronous-events-occur)

[`func confirmation<R>(Comment?, expectedCount: Int, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, (Confirmation) async throws -> sending R) async rethrows -> R`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-5mqz2)

Confirm that some event occurs during the invocation of a function.

[`func confirmation<R>(Comment?, expectedCount: some RangeExpression<Int> & Sendable & Sequence<Int>, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, (Confirmation) async throws -> sending R) async rethrows -> R`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-l3il)

Confirm that some event occurs during the invocation of a function.

[`struct Confirmation`](https://developer.apple.com/documentation/testing/confirmation)

A type that can be used to confirm that an event occurs zero or more times.

Current page is Testing asynchronous code

## Swift Testing Tags
[Skip Navigation](https://developer.apple.com/documentation/testing/tag/list/tags#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Tag](https://developer.apple.com/documentation/testing/tag)
- [Tag.List](https://developer.apple.com/documentation/testing/tag/list)
- tags

Instance Property

# tags

The list of tags contained in this instance.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var tags: [Tag]
```

## [Discussion](https://developer.apple.com/documentation/testing/tag/list/tags\#discussion)

This preserves the list of the tags exactly as they were originally specified, in their original order, including duplicate entries. To access the complete, unique set of tags applied to a [`Test`](https://developer.apple.com/documentation/testing/test), see [`tags`](https://developer.apple.com/documentation/testing/test/tags).

Current page is tags

## Current Test Case
[Skip Navigation](https://developer.apple.com/documentation/testing/test/case/current#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Test](https://developer.apple.com/documentation/testing/test)
- [Test.Case](https://developer.apple.com/documentation/testing/test/case)
- current

Type Property

# current

The test case that is running on the current task, if any.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
static var current: Test.Case? { get }
```

## [Discussion](https://developer.apple.com/documentation/testing/test/case/current\#discussion)

If the current task is running a test, or is a subtask of another task that is running a test, the value of this property describes the test’s currently-running case. If no test is currently running, the value of this property is `nil`.

If the current task is detached from a task that started running a test, or if the current thread was created without using Swift concurrency (e.g. by using [`Thread.detachNewThread(_:)`](https://developer.apple.com/documentation/foundation/thread/2088563-detachnewthread) or [`DispatchQueue.async(execute:)`](https://developer.apple.com/documentation/dispatch/dispatchqueue/2016103-async)), the value of this property may be `nil`.

Current page is current

## Parallelization Trait
[Skip Navigation](https://developer.apple.com/documentation/testing/parallelizationtrait?changes=__2#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing?changes=__2)
- ParallelizationTrait

Structure

# ParallelizationTrait

A type that defines whether the testing library runs this test serially or in parallel.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct ParallelizationTrait
```

## [Overview](https://developer.apple.com/documentation/testing/parallelizationtrait?changes=__2\#overview)

When you add this trait to a parameterized test function, that test runs its cases serially instead of in parallel. This trait has no effect when you apply it to a non-parameterized test function.

When you add this trait to a test suite, that suite runs its contained test functions (including their cases, when parameterized) and sub-suites serially instead of in parallel. If the sub-suites have children, they also run serially.

This trait does not affect the execution of a test relative to its peers or to unrelated tests. This trait has no effect if you disable test parallelization globally (for example, by passing `--no-parallel` to the `swift test` command.)

To add this trait to a test, use [`serialized`](https://developer.apple.com/documentation/testing/trait/serialized?changes=__2).

## [Topics](https://developer.apple.com/documentation/testing/parallelizationtrait?changes=__2\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/parallelizationtrait?changes=__2\#Instance-Properties)

[`var isRecursive: Bool`](https://developer.apple.com/documentation/testing/parallelizationtrait/isrecursive?changes=__2)

Whether this instance should be applied recursively to child test suites and test functions.

### [Type Aliases](https://developer.apple.com/documentation/testing/parallelizationtrait?changes=__2\#Type-Aliases)

[`typealias TestScopeProvider`](https://developer.apple.com/documentation/testing/parallelizationtrait/testscopeprovider?changes=__2)

The type of the test scope provider for this trait.

### [Default Implementations](https://developer.apple.com/documentation/testing/parallelizationtrait?changes=__2\#Default-Implementations)

[API Reference\\
Trait Implementations](https://developer.apple.com/documentation/testing/parallelizationtrait/trait-implementations?changes=__2)

## [Relationships](https://developer.apple.com/documentation/testing/parallelizationtrait?changes=__2\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/parallelizationtrait?changes=__2\#conforms-to)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable?changes=__2)
- [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait?changes=__2)
- [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait?changes=__2)
- [`Trait`](https://developer.apple.com/documentation/testing/trait?changes=__2)

## [See Also](https://developer.apple.com/documentation/testing/parallelizationtrait?changes=__2\#see-also)

### [Supporting types](https://developer.apple.com/documentation/testing/parallelizationtrait?changes=__2\#Supporting-types)

[`struct Bug`](https://developer.apple.com/documentation/testing/bug?changes=__2)

A type that represents a bug report tracked by a test.

[`struct Comment`](https://developer.apple.com/documentation/testing/comment?changes=__2)

A type that represents a comment related to a test.

[`struct ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait?changes=__2)

A type that defines a condition which must be satisfied for the testing library to enable a test.

[`struct Tag`](https://developer.apple.com/documentation/testing/tag?changes=__2)

A type representing a tag that can be applied to a test.

[`struct List`](https://developer.apple.com/documentation/testing/tag/list?changes=__2)

A type representing one or more tags applied to a test.

[`struct TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait?changes=__2)

A type that defines a time limit to apply to a test.

Current page is ParallelizationTrait

## Condition Trait Overview
[Skip Navigation](https://developer.apple.com/documentation/testing/conditiontrait?changes=_1#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing?changes=_1)
- ConditionTrait

Structure

# ConditionTrait

A type that defines a condition which must be satisfied for the testing library to enable a test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct ConditionTrait
```

## [Mentioned in](https://developer.apple.com/documentation/testing/conditiontrait?changes=_1\#mentions)

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest?changes=_1)

## [Overview](https://developer.apple.com/documentation/testing/conditiontrait?changes=_1\#overview)

To add this trait to a test, use one of the following functions:

- [`enabled(if:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/trait/enabled(if:_:sourcelocation:)?changes=_1)

- [`enabled(_:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/trait/enabled(_:sourcelocation:_:)?changes=_1)

- [`disabled(_:sourceLocation:)`](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:)?changes=_1)

- [`disabled(if:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/trait/disabled(if:_:sourcelocation:)?changes=_1)

- [`disabled(_:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:_:)?changes=_1)


## [Topics](https://developer.apple.com/documentation/testing/conditiontrait?changes=_1\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/conditiontrait?changes=_1\#Instance-Properties)

[`var comments: [Comment]`](https://developer.apple.com/documentation/testing/conditiontrait/comments?changes=_1)

The user-provided comments for this trait.

[`var isRecursive: Bool`](https://developer.apple.com/documentation/testing/conditiontrait/isrecursive?changes=_1)

Whether this instance should be applied recursively to child test suites and test functions.

[`var sourceLocation: SourceLocation`](https://developer.apple.com/documentation/testing/conditiontrait/sourcelocation?changes=_1)

The source location where this trait is specified.

### [Instance Methods](https://developer.apple.com/documentation/testing/conditiontrait?changes=_1\#Instance-Methods)

[`func prepare(for: Test) async throws`](https://developer.apple.com/documentation/testing/conditiontrait/prepare(for:)?changes=_1)

Prepare to run the test that has this trait.

### [Type Aliases](https://developer.apple.com/documentation/testing/conditiontrait?changes=_1\#Type-Aliases)

[`typealias TestScopeProvider`](https://developer.apple.com/documentation/testing/conditiontrait/testscopeprovider?changes=_1)

The type of the test scope provider for this trait.

### [Default Implementations](https://developer.apple.com/documentation/testing/conditiontrait?changes=_1\#Default-Implementations)

[API Reference\\
Trait Implementations](https://developer.apple.com/documentation/testing/conditiontrait/trait-implementations?changes=_1)

## [Relationships](https://developer.apple.com/documentation/testing/conditiontrait?changes=_1\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/conditiontrait?changes=_1\#conforms-to)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable?changes=_1)
- [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait?changes=_1)
- [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait?changes=_1)
- [`Trait`](https://developer.apple.com/documentation/testing/trait?changes=_1)

## [See Also](https://developer.apple.com/documentation/testing/conditiontrait?changes=_1\#see-also)

### [Supporting types](https://developer.apple.com/documentation/testing/conditiontrait?changes=_1\#Supporting-types)

[`struct Bug`](https://developer.apple.com/documentation/testing/bug?changes=_1)

A type that represents a bug report tracked by a test.

[`struct Comment`](https://developer.apple.com/documentation/testing/comment?changes=_1)

A type that represents a comment related to a test.

[`struct ParallelizationTrait`](https://developer.apple.com/documentation/testing/parallelizationtrait?changes=_1)

A type that defines whether the testing library runs this test serially or in parallel.

[`struct Tag`](https://developer.apple.com/documentation/testing/tag?changes=_1)

A type representing a tag that can be applied to a test.

[`struct List`](https://developer.apple.com/documentation/testing/tag/list?changes=_1)

A type representing one or more tags applied to a test.

[`struct TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait?changes=_1)

A type that defines a time limit to apply to a test.

Current page is ConditionTrait

## TestScopeProvider Overview
[Skip Navigation](https://developer.apple.com/documentation/testing/comment/testscopeprovider#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Comment](https://developer.apple.com/documentation/testing/comment)
- Comment.TestScopeProvider

Type Alias

# Comment.TestScopeProvider

The type of the test scope provider for this trait.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
typealias TestScopeProvider = Never
```

## [Discussion](https://developer.apple.com/documentation/testing/comment/testscopeprovider\#discussion)

The default type is `Never`, which can’t be instantiated. The `scopeProvider(for:testCase:)-cjmg` method for any trait with `Never` as its test scope provider type must return `nil`, meaning that the trait doesn’t provide a custom scope for tests it’s applied to.

Current page is Comment.TestScopeProvider

## Bug Identifier Overview
[Skip Navigation](https://developer.apple.com/documentation/testing/bug/id?changes=_6#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing?changes=_6)
- [Bug](https://developer.apple.com/documentation/testing/bug?changes=_6)
- id

Instance Property

# id

A unique identifier in this bug’s associated bug-tracking system, if available.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var id: String?
```

## [Discussion](https://developer.apple.com/documentation/testing/bug/id?changes=_6\#discussion)

For more information on how the testing library interprets bug identifiers, see [Interpreting bug identifiers](https://developer.apple.com/documentation/testing/bugidentifiers?changes=_6).

Current page is id

## TestScopeProvider Overview
[Skip Navigation](https://developer.apple.com/documentation/testing/timelimittrait/testscopeprovider?language=objc#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing?language=objc)
- [TimeLimitTrait](https://developer.apple.com/documentation/testing/timelimittrait?language=objc)
- TimeLimitTrait.TestScopeProvider

Type Alias

# TimeLimitTrait.TestScopeProvider

The type of the test scope provider for this trait.

iOS 16.0+iPadOS 16.0+Mac Catalyst 16.0+macOS 13.0+tvOS 16.0+visionOSwatchOS 9.0+Swift 6.0+Xcode 16.0+

```
typealias TestScopeProvider = Never
```

## [Discussion](https://developer.apple.com/documentation/testing/timelimittrait/testscopeprovider?language=objc\#discussion)

The default type is `Never`, which can’t be instantiated. The `scopeProvider(for:testCase:)-cjmg` method for any trait with `Never` as its test scope provider type must return `nil`, meaning that the trait doesn’t provide a custom scope for tests it’s applied to.

Current page is TimeLimitTrait.TestScopeProvider

## Test Duration Limit
[Skip Navigation](https://developer.apple.com/documentation/testing/timelimittrait/timelimit?changes=_3#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing?changes=_3)
- [TimeLimitTrait](https://developer.apple.com/documentation/testing/timelimittrait?changes=_3)
- timeLimit

Instance Property

# timeLimit

The maximum amount of time a test may run for before timing out.

iOS 16.0+iPadOS 16.0+Mac Catalyst 16.0+macOS 13.0+tvOS 16.0+visionOSwatchOS 9.0+Swift 6.0+Xcode 16.0+

```
var timeLimit: Duration
```

Current page is timeLimit

## Swift Issue Kind
[Skip Navigation](https://developer.apple.com/documentation/testing/issue/kind-swift.property#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Issue](https://developer.apple.com/documentation/testing/issue)
- kind

Instance Property

# kind

The kind of issue this value represents.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var kind: Issue.Kind
```

Current page is kind

## Time Limit Trait
[Skip Navigation](https://developer.apple.com/documentation/testing/trait/timelimit(_:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Trait](https://developer.apple.com/documentation/testing/trait)
- timeLimit(\_:)

Type Method

# timeLimit(\_:)

Construct a time limit trait that causes a test to time out if it runs for too long.

iOS 16.0+iPadOS 16.0+Mac Catalyst 16.0+macOS 13.0+tvOS 16.0+visionOSwatchOS 9.0+Swift 6.0+Xcode 16.0+

```
static func timeLimit(_ timeLimit: TimeLimitTrait.Duration) -> Self
```

Available when `Self` is `TimeLimitTrait`.

## [Parameters](https://developer.apple.com/documentation/testing/trait/timelimit(_:)\#parameters)

`timeLimit`

The maximum amount of time the test may run for.

## [Return Value](https://developer.apple.com/documentation/testing/trait/timelimit(_:)\#return-value)

An instance of [`TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait).

## [Mentioned in](https://developer.apple.com/documentation/testing/trait/timelimit(_:)\#mentions)

[Limiting the running time of tests](https://developer.apple.com/documentation/testing/limitingexecutiontime)

## [Discussion](https://developer.apple.com/documentation/testing/trait/timelimit(_:)\#discussion)

Test timeouts do not support high-precision, arbitrarily short durations due to variability in testing environments. You express the duration in minutes, with a minimum duration of one minute.

When you associate this trait with a test, that test must complete within a time limit of, at most, `timeLimit`. If the test runs longer, the testing library records a [`Issue.Kind.timeLimitExceeded(timeLimitComponents:)`](https://developer.apple.com/documentation/testing/issue/kind-swift.enum/timelimitexceeded(timelimitcomponents:)) issue, which it treats as a test failure.

The testing library can use a shorter time limit than that specified by `timeLimit` if you configure it to enforce a maximum per-test limit. When you configure a maximum per-test limit, the time limit of the test this trait is applied to is the shorter of `timeLimit` and the maximum per-test limit. For information on configuring maximum per-test limits, consult the documentation for the tool you use to run your tests.

If a test is parameterized, this time limit is applied to each of its test cases individually. If a test has more than one time limit associated with it, the testing library uses the shortest time limit.

## [See Also](https://developer.apple.com/documentation/testing/trait/timelimit(_:)\#see-also)

### [Customizing runtime behaviors](https://developer.apple.com/documentation/testing/trait/timelimit(_:)\#Customizing-runtime-behaviors)

[Enabling and disabling tests](https://developer.apple.com/documentation/testing/enablinganddisabling)

Conditionally enable or disable individual tests before they run.

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

Current page is timeLimit(\_:)

## Swift Testing Comment
[Skip Navigation](https://developer.apple.com/documentation/testing/comment/rawvalue-swift.property#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Comment](https://developer.apple.com/documentation/testing/comment)
- rawValue

Instance Property

# rawValue

The single comment string that this comment contains.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var rawValue: String
```

## [Discussion](https://developer.apple.com/documentation/testing/comment/rawvalue-swift.property\#discussion)

To get the complete set of comments applied to a test, see [`comments`](https://developer.apple.com/documentation/testing/test/comments).

Current page is rawValue

## isRecursive Property Overview
[Skip Navigation](https://developer.apple.com/documentation/testing/timelimittrait/isrecursive?language=objc#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing?language=objc)
- [TimeLimitTrait](https://developer.apple.com/documentation/testing/timelimittrait?language=objc)
- isRecursive

Instance Property

# isRecursive

Whether this instance should be applied recursively to child test suites and test functions.

iOS 16.0+iPadOS 16.0+Mac Catalyst 16.0+macOS 13.0+tvOS 16.0+visionOSwatchOS 9.0+Swift 6.0+Xcode 16.0+

```
var isRecursive: Bool { get }
```

## [Discussion](https://developer.apple.com/documentation/testing/timelimittrait/isrecursive?language=objc\#discussion)

If the value is `true`, then the testing library applies this trait recursively to child test suites and test functions. Otherwise, it only applies the trait to the test suite to which you added the trait.

By default, traits are not recursively applied to children.

Current page is isRecursive

## Test Preparation Method
[Skip Navigation](https://developer.apple.com/documentation/testing/conditiontrait/prepare(for:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [ConditionTrait](https://developer.apple.com/documentation/testing/conditiontrait)
- prepare(for:)

Instance Method

# prepare(for:)

Prepare to run the test that has this trait.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
func prepare(for test: Test) async throws
```

## [Parameters](https://developer.apple.com/documentation/testing/conditiontrait/prepare(for:)\#parameters)

`test`

The test that has this trait.

## [Discussion](https://developer.apple.com/documentation/testing/conditiontrait/prepare(for:)\#discussion)

The testing library calls this method after it discovers all tests and their traits, and before it begins to run any tests. Use this method to prepare necessary internal state, or to determine whether the test should run.

The default implementation of this method does nothing.

Current page is prepare(for:)

## Test Preparation Method
[Skip Navigation](https://developer.apple.com/documentation/testing/trait/prepare(for:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Trait](https://developer.apple.com/documentation/testing/trait)
- prepare(for:)

Instance Method

# prepare(for:)

Prepare to run the test that has this trait.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
func prepare(for test: Test) async throws
```

**Required** Default implementation provided.

## [Parameters](https://developer.apple.com/documentation/testing/trait/prepare(for:)\#parameters)

`test`

The test that has this trait.

## [Discussion](https://developer.apple.com/documentation/testing/trait/prepare(for:)\#discussion)

The testing library calls this method after it discovers all tests and their traits, and before it begins to run any tests. Use this method to prepare necessary internal state, or to determine whether the test should run.

The default implementation of this method does nothing.

## [Default Implementations](https://developer.apple.com/documentation/testing/trait/prepare(for:)\#default-implementations)

### [Trait Implementations](https://developer.apple.com/documentation/testing/trait/prepare(for:)\#Trait-Implementations)

[`func prepare(for: Test) async throws`](https://developer.apple.com/documentation/testing/trait/prepare(for:)-4pe01)

Prepare to run the test that has this trait.

## [See Also](https://developer.apple.com/documentation/testing/trait/prepare(for:)\#see-also)

### [Running code before and after a test or suite](https://developer.apple.com/documentation/testing/trait/prepare(for:)\#Running-code-before-and-after-a-test-or-suite)

[`protocol TestScoping`](https://developer.apple.com/documentation/testing/testscoping)

A protocol that tells the test runner to run custom code before or after it runs a test suite or test function.

[`func scopeProvider(for: Test, testCase: Test.Case?) -> Self.TestScopeProvider?`](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:))

Get this trait’s scope provider for the specified test and optional test case.

**Required** Default implementations provided.

[`associatedtype TestScopeProvider : TestScoping = Never`](https://developer.apple.com/documentation/testing/trait/testscopeprovider)

The type of the test scope provider for this trait.

**Required**

Current page is prepare(for:)

## Swift Testing Tags
[Skip Navigation](https://developer.apple.com/documentation/testing/trait/tags(_:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Trait](https://developer.apple.com/documentation/testing/trait)
- tags(\_:)

Type Method

# tags(\_:)

Construct a list of tags to apply to a test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
static func tags(_ tags: Tag...) -> Self
```

Available when `Self` is `Tag.List`.

## [Parameters](https://developer.apple.com/documentation/testing/trait/tags(_:)\#parameters)

`tags`

The list of tags to apply to the test.

## [Return Value](https://developer.apple.com/documentation/testing/trait/tags(_:)\#return-value)

An instance of [`Tag.List`](https://developer.apple.com/documentation/testing/tag/list) containing the specified tags.

## [Mentioned in](https://developer.apple.com/documentation/testing/trait/tags(_:)\#mentions)

[Organizing test functions with suite types](https://developer.apple.com/documentation/testing/organizingtests)

[Defining test functions](https://developer.apple.com/documentation/testing/definingtests)

[Adding tags to tests](https://developer.apple.com/documentation/testing/addingtags)

## [See Also](https://developer.apple.com/documentation/testing/trait/tags(_:)\#see-also)

### [Categorizing tests and adding information](https://developer.apple.com/documentation/testing/trait/tags(_:)\#Categorizing-tests-and-adding-information)

[`var comments: [Comment]`](https://developer.apple.com/documentation/testing/trait/comments)

The user-provided comments for this trait.

**Required** Default implementation provided.

Current page is tags(\_:)

## Swift Testing ID
[Skip Navigation](https://developer.apple.com/documentation/testing/test/id-swift.property#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Test](https://developer.apple.com/documentation/testing/test)
- id

Instance Property

# id

The stable identity of the entity associated with this instance.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var id: Test.ID { get }
```

Current page is id

## Swift Test Description
[Skip Navigation](https://developer.apple.com/documentation/testing/customteststringconvertible/testdescription-3ar66?changes=_1#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing?changes=_1)
- [CustomTestStringConvertible](https://developer.apple.com/documentation/testing/customteststringconvertible?changes=_1)
- testDescription

Instance Property

# testDescription

A description of this instance to use when presenting it in a test’s output.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
var testDescription: String { get }
```

Available when `Self` conforms to `StringProtocol`.

## [Discussion](https://developer.apple.com/documentation/testing/customteststringconvertible/testdescription-3ar66?changes=_1\#discussion)

Do not use this property directly. To get the test description of a value, use `Swift/String/init(describingForTest:)`.

Current page is testDescription

## Bug Tracking Method
[Skip Navigation](https://developer.apple.com/documentation/testing/trait/bug(_:_:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Trait](https://developer.apple.com/documentation/testing/trait)
- bug(\_:\_:)

Type Method

# bug(\_:\_:)

Constructs a bug to track with a test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
static func bug(
    _ url: String,
    _ title: Comment? = nil
) -> Self
```

Available when `Self` is `Bug`.

## [Parameters](https://developer.apple.com/documentation/testing/trait/bug(_:_:)\#parameters)

`url`

A URL that refers to this bug in the associated bug-tracking system.

`title`

Optionally, the human-readable title of the bug.

## [Return Value](https://developer.apple.com/documentation/testing/trait/bug(_:_:)\#return-value)

An instance of [`Bug`](https://developer.apple.com/documentation/testing/bug) that represents the specified bug.

## [Mentioned in](https://developer.apple.com/documentation/testing/trait/bug(_:_:)\#mentions)

[Associating bugs with tests](https://developer.apple.com/documentation/testing/associatingbugs)

[Enabling and disabling tests](https://developer.apple.com/documentation/testing/enablinganddisabling)

[Interpreting bug identifiers](https://developer.apple.com/documentation/testing/bugidentifiers)

## [See Also](https://developer.apple.com/documentation/testing/trait/bug(_:_:)\#see-also)

### [Annotating tests](https://developer.apple.com/documentation/testing/trait/bug(_:_:)\#Annotating-tests)

[Adding tags to tests](https://developer.apple.com/documentation/testing/addingtags)

Use tags to provide semantic information for organization, filtering, and customizing appearances.

[Adding comments to tests](https://developer.apple.com/documentation/testing/addingcomments)

Add comments to provide useful information about tests.

[Associating bugs with tests](https://developer.apple.com/documentation/testing/associatingbugs)

Associate bugs uncovered or verified by tests.

[Interpreting bug identifiers](https://developer.apple.com/documentation/testing/bugidentifiers)

Examine how the testing library interprets bug identifiers provided by developers.

[`macro Tag()`](https://developer.apple.com/documentation/testing/tag())

Declare a tag that can be applied to a test function or test suite.

[`static func bug(String?, id: String, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-10yf5)

Constructs a bug to track with a test.

[`static func bug(String?, id: some Numeric, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-3vtpl)

Constructs a bug to track with a test.

Current page is bug(\_:\_:)

## Record Test Issues
[Skip Navigation](https://developer.apple.com/documentation/testing/issue/record(_:sourcelocation:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Issue](https://developer.apple.com/documentation/testing/issue)
- record(\_:sourceLocation:)

Type Method

# record(\_:sourceLocation:)

Record an issue when a running test fails unexpectedly.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
@discardableResult
static func record(
    _ comment: Comment? = nil,
    sourceLocation: SourceLocation = #_sourceLocation
) -> Issue
```

## [Parameters](https://developer.apple.com/documentation/testing/issue/record(_:sourcelocation:)\#parameters)

`comment`

A comment describing the expectation.

`sourceLocation`

The source location to which the issue should be attributed.

## [Return Value](https://developer.apple.com/documentation/testing/issue/record(_:sourcelocation:)\#return-value)

The issue that was recorded.

## [Mentioned in](https://developer.apple.com/documentation/testing/issue/record(_:sourcelocation:)\#mentions)

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

## [Discussion](https://developer.apple.com/documentation/testing/issue/record(_:sourcelocation:)\#discussion)

Use this function if, while running a test, an issue occurs that cannot be represented as an expectation (using the [`expect(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:)) or [`require(_:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q) macros.)

Current page is record(\_:sourceLocation:)

## Scope Provider Method
[Skip Navigation](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Trait](https://developer.apple.com/documentation/testing/trait)
- scopeProvider(for:testCase:)

Instance Method

# scopeProvider(for:testCase:)

Get this trait’s scope provider for the specified test and optional test case.

Swift 6.1+Xcode 16.3+

```
func scopeProvider(
    for test: Test,
    testCase: Test.Case?
) -> Self.TestScopeProvider?
```

**Required** Default implementations provided.

## [Parameters](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)\#parameters)

`test`

The test for which a scope provider is being requested.

`testCase`

The test case for which a scope provider is being requested, if any. When `test` represents a suite, the value of this argument is `nil`.

## [Return Value](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)\#return-value)

A value conforming to [`TestScopeProvider`](https://developer.apple.com/documentation/testing/trait/testscopeprovider) which you use to provide custom scoping for `test` or `testCase`. Returns `nil` if the trait doesn’t provide any custom scope for the test or test case.

## [Discussion](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)\#discussion)

If this trait’s type conforms to [`TestScoping`](https://developer.apple.com/documentation/testing/testscoping), the default value returned by this method depends on the values of `test` and `testCase`:

- If `test` represents a suite, this trait must conform to [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait). If the value of this suite trait’s [`isRecursive`](https://developer.apple.com/documentation/testing/suitetrait/isrecursive) property is `true`, then this method returns `nil`, and the suite trait provides its custom scope once for each test function the test suite contains. If the value of [`isRecursive`](https://developer.apple.com/documentation/testing/suitetrait/isrecursive) is `false`, this method returns `self`, and the suite trait provides its custom scope once for the entire test suite.

- If `test` represents a test function, this trait also conforms to [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait). If `testCase` is `nil`, this method returns `nil`; otherwise, it returns `self`. This means that by default, a trait which is applied to or inherited by a test function provides its custom scope once for each of that function’s cases.


A trait may override this method to further customize the default behaviors above. For example, if a trait needs to provide custom test scope both once per-suite and once per-test function in that suite, it implements the method to return a non- `nil` scope provider under those conditions.

A trait may also implement this method and return `nil` if it determines that it does not need to provide a custom scope for a particular test at runtime, even if the test has the trait applied. This can improve performance and make diagnostics clearer by avoiding an unnecessary call to [`provideScope(for:testCase:performing:)`](https://developer.apple.com/documentation/testing/testscoping/providescope(for:testcase:performing:)).

If this trait’s type does not conform to [`TestScoping`](https://developer.apple.com/documentation/testing/testscoping) and its associated [`TestScopeProvider`](https://developer.apple.com/documentation/testing/trait/testscopeprovider) type is the default `Never`, then this method returns `nil` by default. This means that instances of this trait don’t provide a custom scope for tests to which they’re applied.

## [Default Implementations](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)\#default-implementations)

### [Trait Implementations](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)\#Trait-Implementations)

[`func scopeProvider(for: Test, testCase: Test.Case?) -> Never?`](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)-9fxg4)

Get this trait’s scope provider for the specified test or test case.

[`func scopeProvider(for: Test, testCase: Test.Case?) -> Self?`](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)-1z8kh)

Get this trait’s scope provider for the specified test or test case.

[`func scopeProvider(for: Test, testCase: Test.Case?) -> Self?`](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)-inmj)

Get this trait’s scope provider for the specified test and optional test case.

## [See Also](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)\#see-also)

### [Running code before and after a test or suite](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)\#Running-code-before-and-after-a-test-or-suite)

[`protocol TestScoping`](https://developer.apple.com/documentation/testing/testscoping)

A protocol that tells the test runner to run custom code before or after it runs a test suite or test function.

[`associatedtype TestScopeProvider : TestScoping = Never`](https://developer.apple.com/documentation/testing/trait/testscopeprovider)

The type of the test scope provider for this trait.

**Required**

[`func prepare(for: Test) async throws`](https://developer.apple.com/documentation/testing/trait/prepare(for:))

Prepare to run the test that has this trait.

**Required** Default implementation provided.

Current page is scopeProvider(for:testCase:)

## Swift Testing Expectation
[Skip Navigation](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- expect(\_:\_:sourceLocation:)

Macro

# expect(\_:\_:sourceLocation:)

Check that an expectation has passed after a condition has been evaluated.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
@freestanding(expression)
macro expect(
    _ condition: Bool,
    _ comment: @autoclosure () -> Comment? = nil,
    sourceLocation: SourceLocation = #_sourceLocation
)
```

## [Parameters](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:)\#parameters)

`condition`

The condition to be evaluated.

`comment`

A comment describing the expectation.

`sourceLocation`

The source location to which recorded expectations and issues should be attributed.

## [Mentioned in](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:)\#mentions)

[Testing for errors in Swift code](https://developer.apple.com/documentation/testing/testing-for-errors-in-swift-code)

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

## [Overview](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:)\#overview)

If `condition` evaluates to `false`, an [`Issue`](https://developer.apple.com/documentation/testing/issue) is recorded for the test that is running in the current task.

## [See Also](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:)\#see-also)

### [Checking expectations](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:)\#Checking-expectations)

[`macro require(Bool, @autoclosure () -> Comment?, sourceLocation: SourceLocation)`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q)

Check that an expectation has passed after a condition has been evaluated and throw an error if it failed.

[`macro require<T>(T?, @autoclosure () -> Comment?, sourceLocation: SourceLocation) -> T`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-6w9oo)

Unwrap an optional value or, if it is `nil`, fail and throw an error.

Current page is expect(\_:\_:sourceLocation:)

## System Issue Kind
[Skip Navigation](https://developer.apple.com/documentation/testing/issue/kind-swift.enum/system#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Issue](https://developer.apple.com/documentation/testing/issue)
- [Issue.Kind](https://developer.apple.com/documentation/testing/issue/kind-swift.enum)
- Issue.Kind.system

Case

# Issue.Kind.system

An issue due to a failure in the underlying system, not due to a failure within the tests being run.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
case system
```

Current page is Issue.Kind.system

## Disable Test Condition
[Skip Navigation](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Trait](https://developer.apple.com/documentation/testing/trait)
- disabled(\_:sourceLocation:)

Type Method

# disabled(\_:sourceLocation:)

Constructs a condition trait that disables a test unconditionally.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
static func disabled(
    _ comment: Comment? = nil,
    sourceLocation: SourceLocation = #_sourceLocation
) -> Self
```

Available when `Self` is `ConditionTrait`.

## [Parameters](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:)\#parameters)

`comment`

An optional comment that describes this trait.

`sourceLocation`

The source location of the trait.

## [Return Value](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:)\#return-value)

An instance of [`ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait) that always disables the test to which it is added.

## [Mentioned in](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:)\#mentions)

[Enabling and disabling tests](https://developer.apple.com/documentation/testing/enablinganddisabling)

[Organizing test functions with suite types](https://developer.apple.com/documentation/testing/organizingtests)

## [See Also](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:)\#see-also)

### [Customizing runtime behaviors](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:)\#Customizing-runtime-behaviors)

[Enabling and disabling tests](https://developer.apple.com/documentation/testing/enablinganddisabling)

Conditionally enable or disable individual tests before they run.

[Limiting the running time of tests](https://developer.apple.com/documentation/testing/limitingexecutiontime)

Set limits on how long a test can run for until it fails.

[`static func enabled(if: @autoclosure () throws -> Bool, Comment?, sourceLocation: SourceLocation) -> Self`](https://developer.apple.com/documentation/testing/trait/enabled(if:_:sourcelocation:))

Constructs a condition trait that disables a test if it returns `false`.

[`static func enabled(Comment?, sourceLocation: SourceLocation, () async throws -> Bool) -> Self`](https://developer.apple.com/documentation/testing/trait/enabled(_:sourcelocation:_:))

Constructs a condition trait that disables a test if it returns `false`.

[`static func disabled(if: @autoclosure () throws -> Bool, Comment?, sourceLocation: SourceLocation) -> Self`](https://developer.apple.com/documentation/testing/trait/disabled(if:_:sourcelocation:))

Constructs a condition trait that disables a test if its value is true.

[`static func disabled(Comment?, sourceLocation: SourceLocation, () async throws -> Bool) -> Self`](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:_:))

Constructs a condition trait that disables a test if its value is true.

[`static func timeLimit(TimeLimitTrait.Duration) -> Self`](https://developer.apple.com/documentation/testing/trait/timelimit(_:))

Construct a time limit trait that causes a test to time out if it runs for too long.

Current page is disabled(\_:sourceLocation:)

## Hashing Method
[Skip Navigation](https://developer.apple.com/documentation/testing/tag/list/hash(into:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Tag](https://developer.apple.com/documentation/testing/tag)
- [Tag.List](https://developer.apple.com/documentation/testing/tag/list)
- hash(into:)

Instance Method

# hash(into:)

Hashes the essential components of this value by feeding them into the given hasher.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
func hash(into hasher: inout Hasher)
```

## [Parameters](https://developer.apple.com/documentation/testing/tag/list/hash(into:)\#parameters)

`hasher`

The hasher to use when combining the components of this instance.

## [Discussion](https://developer.apple.com/documentation/testing/tag/list/hash(into:)\#discussion)

Implement this method to conform to the `Hashable` protocol. The components used for hashing must be the same as the components compared in your type’s `==` operator implementation. Call `hasher.combine(_:)` with each of these components.

Current page is hash(into:)

## Tag Comparison Operator
[Skip Navigation](https://developer.apple.com/documentation/testing/tag/_(_:_:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Tag](https://developer.apple.com/documentation/testing/tag)
- <(\_:\_:)

Operator

# <(\_:\_:)

Returns a Boolean value indicating whether the value of the first argument is less than that of the second argument.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
static func < (lhs: Tag, rhs: Tag) -> Bool
```

## [Parameters](https://developer.apple.com/documentation/testing/tag/_(_:_:)\#parameters)

`lhs`

A value to compare.

`rhs`

Another value to compare.

## [Discussion](https://developer.apple.com/documentation/testing/tag/_(_:_:)\#discussion)

This function is the only requirement of the `Comparable` protocol. The remainder of the relational operator functions are implemented by the standard library for any type that conforms to `Comparable`.

Current page is <(\_:\_:)

## Test Execution Control
[Skip Navigation](https://developer.apple.com/documentation/testing/parallelization?changes=_3#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing?changes=_3)
- [Traits](https://developer.apple.com/documentation/testing/traits?changes=_3)
- Running tests serially or in parallel

Article

# Running tests serially or in parallel

Control whether tests run serially or in parallel.

## [Overview](https://developer.apple.com/documentation/testing/parallelization?changes=_3\#Overview)

By default, tests run in parallel with respect to each other. Parallelization is accomplished by the testing library using task groups, and tests generally all run in the same process. The number of tests that run concurrently is controlled by the Swift runtime.

## [Disabling parallelization](https://developer.apple.com/documentation/testing/parallelization?changes=_3\#Disabling-parallelization)

Parallelization can be disabled on a per-function or per-suite basis using the [`serialized`](https://developer.apple.com/documentation/testing/trait/serialized?changes=_3) trait:

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

## [See Also](https://developer.apple.com/documentation/testing/parallelization?changes=_3\#see-also)

### [Running tests serially or in parallel](https://developer.apple.com/documentation/testing/parallelization?changes=_3\#Running-tests-serially-or-in-parallel)

[`static var serialized: ParallelizationTrait`](https://developer.apple.com/documentation/testing/trait/serialized?changes=_3)

A trait that serializes the test to which it is applied.

Current page is Running tests serially or in parallel

## Scope Provider Method
[Skip Navigation](https://developer.apple.com/documentation/testing/conditiontrait/scopeprovider(for:testcase:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [ConditionTrait](https://developer.apple.com/documentation/testing/conditiontrait)
- scopeProvider(for:testCase:)

Instance Method

# scopeProvider(for:testCase:)

Get this trait’s scope provider for the specified test or test case.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
func scopeProvider(
    for test: Test,
    testCase: Test.Case?
) -> Never?
```

Available when `TestScopeProvider` is `Never`.

## [Parameters](https://developer.apple.com/documentation/testing/conditiontrait/scopeprovider(for:testcase:)\#parameters)

`test`

The test for which the testing library requests a scope provider.

`testCase`

The test case for which the testing library requests a scope provider, if any. When `test` represents a suite, the value of this argument is `nil`.

## [Discussion](https://developer.apple.com/documentation/testing/conditiontrait/scopeprovider(for:testcase:)\#discussion)

The testing library uses this implementation of [`scopeProvider(for:testCase:)`](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)) when the trait type’s associated [`TestScopeProvider`](https://developer.apple.com/documentation/testing/trait/testscopeprovider) type is `Never`.

Current page is scopeProvider(for:testCase:)

## Swift Test Issues
[Skip Navigation](https://developer.apple.com/documentation/testing/issue?changes=_8#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing?changes=_8)
- Issue

Structure

# Issue

A type describing a failure or warning which occurred during a test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct Issue
```

## [Mentioned in](https://developer.apple.com/documentation/testing/issue?changes=_8\#mentions)

[Associating bugs with tests](https://developer.apple.com/documentation/testing/associatingbugs?changes=_8)

[Interpreting bug identifiers](https://developer.apple.com/documentation/testing/bugidentifiers?changes=_8)

## [Topics](https://developer.apple.com/documentation/testing/issue?changes=_8\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/issue?changes=_8\#Instance-Properties)

[`var comments: [Comment]`](https://developer.apple.com/documentation/testing/issue/comments?changes=_8)

Any comments provided by the developer and associated with this issue.

[`var error: (any Error)?`](https://developer.apple.com/documentation/testing/issue/error?changes=_8)

The error which was associated with this issue, if any.

[`var kind: Issue.Kind`](https://developer.apple.com/documentation/testing/issue/kind-swift.property?changes=_8)

The kind of issue this value represents.

[`var sourceLocation: SourceLocation?`](https://developer.apple.com/documentation/testing/issue/sourcelocation?changes=_8)

The location in source where this issue occurred, if available.

### [Type Methods](https://developer.apple.com/documentation/testing/issue?changes=_8\#Type-Methods)

[`static func record(any Error, Comment?, sourceLocation: SourceLocation) -> Issue`](https://developer.apple.com/documentation/testing/issue/record(_:_:sourcelocation:)?changes=_8)

Record a new issue when a running test unexpectedly catches an error.

[`static func record(Comment?, sourceLocation: SourceLocation) -> Issue`](https://developer.apple.com/documentation/testing/issue/record(_:sourcelocation:)?changes=_8)

Record an issue when a running test fails unexpectedly.

### [Enumerations](https://developer.apple.com/documentation/testing/issue?changes=_8\#Enumerations)

[`enum Kind`](https://developer.apple.com/documentation/testing/issue/kind-swift.enum?changes=_8)

Kinds of issues which may be recorded.

### [Default Implementations](https://developer.apple.com/documentation/testing/issue?changes=_8\#Default-Implementations)

[API Reference\\
CustomDebugStringConvertible Implementations](https://developer.apple.com/documentation/testing/issue/customdebugstringconvertible-implementations?changes=_8)

[API Reference\\
CustomStringConvertible Implementations](https://developer.apple.com/documentation/testing/issue/customstringconvertible-implementations?changes=_8)

## [Relationships](https://developer.apple.com/documentation/testing/issue?changes=_8\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/issue?changes=_8\#conforms-to)

- [`Copyable`](https://developer.apple.com/documentation/Swift/Copyable?changes=_8)
- [`CustomDebugStringConvertible`](https://developer.apple.com/documentation/Swift/CustomDebugStringConvertible?changes=_8)
- [`CustomStringConvertible`](https://developer.apple.com/documentation/Swift/CustomStringConvertible?changes=_8)
- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable?changes=_8)

Current page is Issue

## Confirmation Testing
[Skip Navigation](https://developer.apple.com/documentation/testing/confirmation?language=objc#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing?language=objc)
- Confirmation

Structure

# Confirmation

A type that can be used to confirm that an event occurs zero or more times.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct Confirmation
```

## [Mentioned in](https://developer.apple.com/documentation/testing/confirmation?language=objc\#mentions)

[Testing asynchronous code](https://developer.apple.com/documentation/testing/testing-asynchronous-code?language=objc)

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest?language=objc)

## [Topics](https://developer.apple.com/documentation/testing/confirmation?language=objc\#topics)

### [Instance Methods](https://developer.apple.com/documentation/testing/confirmation?language=objc\#Instance-Methods)

[`func callAsFunction(count: Int)`](https://developer.apple.com/documentation/testing/confirmation/callasfunction(count:)?language=objc)

Confirm this confirmation.

[`func confirm(count: Int)`](https://developer.apple.com/documentation/testing/confirmation/confirm(count:)?language=objc)

Confirm this confirmation.

## [Relationships](https://developer.apple.com/documentation/testing/confirmation?language=objc\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/confirmation?language=objc\#conforms-to)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable?language=objc)

## [See Also](https://developer.apple.com/documentation/testing/confirmation?language=objc\#see-also)

### [Confirming that asynchronous events occur](https://developer.apple.com/documentation/testing/confirmation?language=objc\#Confirming-that-asynchronous-events-occur)

[Testing asynchronous code](https://developer.apple.com/documentation/testing/testing-asynchronous-code?language=objc)

Validate whether your code causes expected events to happen.

[`func confirmation<R>(Comment?, expectedCount: Int, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, (Confirmation) async throws -> sending R) async rethrows -> R`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-5mqz2?language=objc)

Confirm that some event occurs during the invocation of a function.

[`func confirmation<R>(Comment?, expectedCount: some RangeExpression<Int> & Sendable & Sequence<Int>, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, (Confirmation) async throws -> sending R) async rethrows -> R`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-l3il?language=objc)

Confirm that some event occurs during the invocation of a function.

Current page is Confirmation

## Parameterized Test Macro
[Skip Navigation](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Test(\_:\_:arguments:)

Macro

# Test(\_:\_:arguments:)

Declare a test parameterized over two zipped collections of values.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
@attached(peer)
macro Test<C1, C2>(
    _ displayName: String? = nil,
    _ traits: any TestTrait...,
    arguments zippedCollections: Zip2Sequence<C1, C2>
) where C1 : Collection, C1 : Sendable, C2 : Collection, C2 : Sendable, C1.Element : Sendable, C2.Element : Sendable
```

## [Parameters](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok\#parameters)

`displayName`

The customized display name of this test. If the value of this argument is `nil`, the display name of the test is derived from the associated function’s name.

`traits`

Zero or more traits to apply to this test.

`zippedCollections`

Two zipped collections of values to pass to `testFunction`.

## [Overview](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok\#overview)

During testing, the associated test function is called once for each element in `zippedCollections`.

## [See Also](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok\#see-also)

### [Related Documentation](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok\#Related-Documentation)

[Defining test functions](https://developer.apple.com/documentation/testing/definingtests)

Define a test function to validate that code is working correctly.

### [Test parameterization](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok\#Test-parameterization)

[Implementing parameterized tests](https://developer.apple.com/documentation/testing/parameterizedtesting)

Specify different input parameters to generate multiple test cases from a test function.

[`macro Test<C>(String?, any TestTrait..., arguments: C)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-8kn7a)

Declare a test parameterized over a collection of values.

[`macro Test<C1, C2>(String?, any TestTrait..., arguments: C1, C2)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:_:))

Declare a test parameterized over two collections of values.

[`protocol CustomTestArgumentEncodable`](https://developer.apple.com/documentation/testing/customtestargumentencodable)

A protocol for customizing how arguments passed to parameterized tests are encoded, which is used to match against when running specific arguments.

[`struct Case`](https://developer.apple.com/documentation/testing/test/case)

A single test case from a parameterized [`Test`](https://developer.apple.com/documentation/testing/test).

Current page is Test(\_:\_:arguments:)

## Known Issue Function
[Skip Navigation](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- withKnownIssue(\_:isIntermittent:sourceLocation:\_:)

Function

# withKnownIssue(\_:isIntermittent:sourceLocation:\_:)

Invoke a function that has a known issue that is expected to occur during its execution.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
func withKnownIssue(
    _ comment: Comment? = nil,
    isIntermittent: Bool = false,
    sourceLocation: SourceLocation = #_sourceLocation,
    _ body: () throws -> Void
)
```

## [Parameters](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:)\#parameters)

`comment`

An optional comment describing the known issue.

`isIntermittent`

Whether or not the known issue occurs intermittently. If this argument is `true` and the known issue does not occur, no secondary issue is recorded.

`sourceLocation`

The source location to which any recorded issues should be attributed.

`body`

The function to invoke.

## [Mentioned in](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:)\#mentions)

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

## [Discussion](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:)\#discussion)

Use this function when a test is known to raise one or more issues that should not cause the test to fail. For example:

```
@Test func example() {
  withKnownIssue {
    try flakyCall()
  }
}

```

Because all errors thrown by `body` are caught as known issues, this function is not throwing. If only some errors or issues are known to occur while others should continue to cause test failures, use [`withKnownIssue(_:isIntermittent:sourceLocation:_:when:matching:)`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:when:matching:)) instead.

## [See Also](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:)\#see-also)

### [Recording known issues in tests](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:)\#Recording-known-issues-in-tests)

[`func withKnownIssue(Comment?, isIntermittent: Bool, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, () async throws -> Void) async`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:isolation:sourcelocation:_:))

Invoke a function that has a known issue that is expected to occur during its execution.

[`func withKnownIssue(Comment?, isIntermittent: Bool, sourceLocation: SourceLocation, () throws -> Void, when: () -> Bool, matching: KnownIssueMatcher) rethrows`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:when:matching:))

Invoke a function that has a known issue that is expected to occur during its execution.

[`func withKnownIssue(Comment?, isIntermittent: Bool, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, () async throws -> Void, when: () async -> Bool, matching: KnownIssueMatcher) async rethrows`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:isolation:sourcelocation:_:when:matching:))

Invoke a function that has a known issue that is expected to occur during its execution.

[`typealias KnownIssueMatcher`](https://developer.apple.com/documentation/testing/knownissuematcher)

A function that is used to match known issues.

Current page is withKnownIssue(\_:isIntermittent:sourceLocation:\_:)

## Event Confirmation Function
[Skip Navigation](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:sourcelocation:_:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Expectations and confirmations](https://developer.apple.com/documentation/testing/expectations)
- confirmation(\_:expectedCount:sourceLocation:\_:)

Function

# confirmation(\_:expectedCount:sourceLocation:\_:)

Confirm that some event occurs during the invocation of a function.

Swift 6.0+Xcode 16.0+

```
func confirmation<R>(
    _ comment: Comment? = nil,
    expectedCount: Int = 1,
    sourceLocation: SourceLocation = #_sourceLocation,
    _ body: (Confirmation) async throws -> R
) async rethrows -> R
```

## [Parameters](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:sourcelocation:_:)\#parameters)

`comment`

An optional comment to apply to any issues generated by this function.

`expectedCount`

The number of times the expected event should occur when `body` is invoked. The default value of this argument is `1`, indicating that the event should occur exactly once. Pass `0` if the event should _never_ occur when `body` is invoked.

`sourceLocation`

The source location to which any recorded issues should be attributed.

`body`

The function to invoke.

## [Return Value](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:sourcelocation:_:)\#return-value)

Whatever is returned by `body`.

## [Mentioned in](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:sourcelocation:_:)\#mentions)

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

[Testing asynchronous code](https://developer.apple.com/documentation/testing/testing-asynchronous-code)

## [Discussion](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:sourcelocation:_:)\#discussion)

Use confirmations to check that an event occurs while a test is running in complex scenarios where `#expect()` and `#require()` are insufficient. For example, a confirmation may be useful when an expected event occurs:

- In a context that cannot be awaited by the calling function such as an event handler or delegate callback;

- More than once, or never; or

- As a callback that is invoked as part of a larger operation.


To use a confirmation, pass a closure containing the work to be performed. The testing library will then pass an instance of [`Confirmation`](https://developer.apple.com/documentation/testing/confirmation) to the closure. Every time the event in question occurs, the closure should call the confirmation:

```
let n = 10
await confirmation("Baked buns", expectedCount: n) { bunBaked in
  foodTruck.eventHandler = { event in
    if event == .baked(.cinnamonBun) {
      bunBaked()
    }
  }
  await foodTruck.bake(.cinnamonBun, count: n)
}

```

When the closure returns, the testing library checks if the confirmation’s preconditions have been met, and records an issue if they have not.

## [See Also](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:sourcelocation:_:)\#see-also)

### [Confirming that asynchronous events occur](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:sourcelocation:_:)\#Confirming-that-asynchronous-events-occur)

[Testing asynchronous code](https://developer.apple.com/documentation/testing/testing-asynchronous-code)

Validate whether your code causes expected events to happen.

[`struct Confirmation`](https://developer.apple.com/documentation/testing/confirmation)

A type that can be used to confirm that an event occurs zero or more times.

Current page is confirmation(\_:expectedCount:sourceLocation:\_:)

## Disable Test Trait
[Skip Navigation](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:_:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Trait](https://developer.apple.com/documentation/testing/trait)
- disabled(\_:sourceLocation:\_:)

Type Method

# disabled(\_:sourceLocation:\_:)

Constructs a condition trait that disables a test if its value is true.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
static func disabled(
    _ comment: Comment? = nil,
    sourceLocation: SourceLocation = #_sourceLocation,
    _ condition: @escaping () async throws -> Bool
) -> Self
```

Available when `Self` is `ConditionTrait`.

## [Parameters](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:_:)\#parameters)

`comment`

An optional comment that describes this trait.

`sourceLocation`

The source location of the trait.

`condition`

A closure that contains the trait’s custom condition logic. If this closure returns `false`, the trait allows the test to run. Otherwise, the testing library skips the test.

## [Return Value](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:_:)\#return-value)

An instance of [`ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait) that evaluates the specified closure.

## [See Also](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:_:)\#see-also)

### [Customizing runtime behaviors](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:_:)\#Customizing-runtime-behaviors)

[Enabling and disabling tests](https://developer.apple.com/documentation/testing/enablinganddisabling)

Conditionally enable or disable individual tests before they run.

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

[`static func timeLimit(TimeLimitTrait.Duration) -> Self`](https://developer.apple.com/documentation/testing/trait/timelimit(_:))

Construct a time limit trait that causes a test to time out if it runs for too long.

Current page is disabled(\_:sourceLocation:\_:)

## Test Disabling Trait
[Skip Navigation](https://developer.apple.com/documentation/testing/trait/disabled(if:_:sourcelocation:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Trait](https://developer.apple.com/documentation/testing/trait)
- disabled(if:\_:sourceLocation:)

Type Method

# disabled(if:\_:sourceLocation:)

Constructs a condition trait that disables a test if its value is true.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
static func disabled(
    if condition: @autoclosure @escaping () throws -> Bool,
    _ comment: Comment? = nil,
    sourceLocation: SourceLocation = #_sourceLocation
) -> Self
```

Available when `Self` is `ConditionTrait`.

## [Parameters](https://developer.apple.com/documentation/testing/trait/disabled(if:_:sourcelocation:)\#parameters)

`condition`

A closure that contains the trait’s custom condition logic. If this closure returns `false`, the trait allows the test to run. Otherwise, the testing library skips the test.

`comment`

An optional comment that describes this trait.

`sourceLocation`

The source location of the trait.

## [Return Value](https://developer.apple.com/documentation/testing/trait/disabled(if:_:sourcelocation:)\#return-value)

An instance of [`ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait) that evaluates the closure you provide.

## [See Also](https://developer.apple.com/documentation/testing/trait/disabled(if:_:sourcelocation:)\#see-also)

### [Customizing runtime behaviors](https://developer.apple.com/documentation/testing/trait/disabled(if:_:sourcelocation:)\#Customizing-runtime-behaviors)

[Enabling and disabling tests](https://developer.apple.com/documentation/testing/enablinganddisabling)

Conditionally enable or disable individual tests before they run.

[Limiting the running time of tests](https://developer.apple.com/documentation/testing/limitingexecutiontime)

Set limits on how long a test can run for until it fails.

[`static func enabled(if: @autoclosure () throws -> Bool, Comment?, sourceLocation: SourceLocation) -> Self`](https://developer.apple.com/documentation/testing/trait/enabled(if:_:sourcelocation:))

Constructs a condition trait that disables a test if it returns `false`.

[`static func enabled(Comment?, sourceLocation: SourceLocation, () async throws -> Bool) -> Self`](https://developer.apple.com/documentation/testing/trait/enabled(_:sourcelocation:_:))

Constructs a condition trait that disables a test if it returns `false`.

[`static func disabled(Comment?, sourceLocation: SourceLocation) -> Self`](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:))

Constructs a condition trait that disables a test unconditionally.

[`static func disabled(Comment?, sourceLocation: SourceLocation, () async throws -> Bool) -> Self`](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:_:))

Constructs a condition trait that disables a test if its value is true.

[`static func timeLimit(TimeLimitTrait.Duration) -> Self`](https://developer.apple.com/documentation/testing/trait/timelimit(_:))

Construct a time limit trait that causes a test to time out if it runs for too long.

Current page is disabled(if:\_:sourceLocation:)

## Condition Trait Management
[Skip Navigation](https://developer.apple.com/documentation/testing/trait/enabled(if:_:sourcelocation:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Trait](https://developer.apple.com/documentation/testing/trait)
- enabled(if:\_:sourceLocation:)

Type Method

# enabled(if:\_:sourceLocation:)

Constructs a condition trait that disables a test if it returns `false`.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
static func enabled(
    if condition: @autoclosure @escaping () throws -> Bool,
    _ comment: Comment? = nil,
    sourceLocation: SourceLocation = #_sourceLocation
) -> Self
```

Available when `Self` is `ConditionTrait`.

## [Parameters](https://developer.apple.com/documentation/testing/trait/enabled(if:_:sourcelocation:)\#parameters)

`condition`

A closure that contains the trait’s custom condition logic. If this closure returns `true`, the trait allows the test to run. Otherwise, the testing library skips the test.

`comment`

An optional comment that describes this trait.

`sourceLocation`

The source location of the trait.

## [Return Value](https://developer.apple.com/documentation/testing/trait/enabled(if:_:sourcelocation:)\#return-value)

An instance of [`ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait) that evaluates the closure you provide.

## [Mentioned in](https://developer.apple.com/documentation/testing/trait/enabled(if:_:sourcelocation:)\#mentions)

[Enabling and disabling tests](https://developer.apple.com/documentation/testing/enablinganddisabling)

## [See Also](https://developer.apple.com/documentation/testing/trait/enabled(if:_:sourcelocation:)\#see-also)

### [Customizing runtime behaviors](https://developer.apple.com/documentation/testing/trait/enabled(if:_:sourcelocation:)\#Customizing-runtime-behaviors)

[Enabling and disabling tests](https://developer.apple.com/documentation/testing/enablinganddisabling)

Conditionally enable or disable individual tests before they run.

[Limiting the running time of tests](https://developer.apple.com/documentation/testing/limitingexecutiontime)

Set limits on how long a test can run for until it fails.

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

Current page is enabled(if:\_:sourceLocation:)

## Swift Testing Macro
[Skip Navigation](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-6w9oo#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- require(\_:\_:sourceLocation:)

Macro

# require(\_:\_:sourceLocation:)

Unwrap an optional value or, if it is `nil`, fail and throw an error.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
@freestanding(expression)
macro require<T>(
    _ optionalValue: T?,
    _ comment: @autoclosure () -> Comment? = nil,
    sourceLocation: SourceLocation = #_sourceLocation
) -> T
```

## [Parameters](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-6w9oo\#parameters)

`optionalValue`

The optional value to be unwrapped.

`comment`

A comment describing the expectation.

`sourceLocation`

The source location to which recorded expectations and issues should be attributed.

## [Return Value](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-6w9oo\#return-value)

The unwrapped value of `optionalValue`.

## [Mentioned in](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-6w9oo\#mentions)

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

## [Overview](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-6w9oo\#overview)

If `optionalValue` is `nil`, an [`Issue`](https://developer.apple.com/documentation/testing/issue) is recorded for the test that is running in the current task and an instance of [`ExpectationFailedError`](https://developer.apple.com/documentation/testing/expectationfailederror) is thrown.

## [See Also](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-6w9oo\#see-also)

### [Checking expectations](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-6w9oo\#Checking-expectations)

[`macro expect(Bool, @autoclosure () -> Comment?, sourceLocation: SourceLocation)`](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:))

Check that an expectation has passed after a condition has been evaluated.

[`macro require(Bool, @autoclosure () -> Comment?, sourceLocation: SourceLocation)`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q)

Check that an expectation has passed after a condition has been evaluated and throw an error if it failed.

Current page is require(\_:\_:sourceLocation:)

## Parameterized Test Declaration
[Skip Navigation](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-8kn7a#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Test(\_:\_:arguments:)

Macro

# Test(\_:\_:arguments:)

Declare a test parameterized over a collection of values.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
@attached(peer)
macro Test<C>(
    _ displayName: String? = nil,
    _ traits: any TestTrait...,
    arguments collection: C
) where C : Collection, C : Sendable, C.Element : Sendable
```

## [Parameters](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-8kn7a\#parameters)

`displayName`

The customized display name of this test. If the value of this argument is `nil`, the display name of the test is derived from the associated function’s name.

`traits`

Zero or more traits to apply to this test.

`collection`

A collection of values to pass to the associated test function.

## [Overview](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-8kn7a\#overview)

During testing, the associated test function is called once for each element in `collection`.

## [See Also](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-8kn7a\#see-also)

### [Related Documentation](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-8kn7a\#Related-Documentation)

[Defining test functions](https://developer.apple.com/documentation/testing/definingtests)

Define a test function to validate that code is working correctly.

### [Test parameterization](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-8kn7a\#Test-parameterization)

[Implementing parameterized tests](https://developer.apple.com/documentation/testing/parameterizedtesting)

Specify different input parameters to generate multiple test cases from a test function.

[`macro Test<C1, C2>(String?, any TestTrait..., arguments: C1, C2)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:_:))

Declare a test parameterized over two collections of values.

[`macro Test<C1, C2>(String?, any TestTrait..., arguments: Zip2Sequence<C1, C2>)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok)

Declare a test parameterized over two zipped collections of values.

[`protocol CustomTestArgumentEncodable`](https://developer.apple.com/documentation/testing/customtestargumentencodable)

A protocol for customizing how arguments passed to parameterized tests are encoded, which is used to match against when running specific arguments.

[`struct Case`](https://developer.apple.com/documentation/testing/test/case)

A single test case from a parameterized [`Test`](https://developer.apple.com/documentation/testing/test).

Current page is Test(\_:\_:arguments:)

## Swift Testing Macro
[Skip Navigation](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- require(\_:\_:sourceLocation:)

Macro

# require(\_:\_:sourceLocation:)

Check that an expectation has passed after a condition has been evaluated and throw an error if it failed.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
@freestanding(expression)
macro require(
    _ condition: Bool,
    _ comment: @autoclosure () -> Comment? = nil,
    sourceLocation: SourceLocation = #_sourceLocation
)
```

## [Parameters](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q\#parameters)

`condition`

The condition to be evaluated.

`comment`

A comment describing the expectation.

`sourceLocation`

The source location to which recorded expectations and issues should be attributed.

## [Mentioned in](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q\#mentions)

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

[Testing for errors in Swift code](https://developer.apple.com/documentation/testing/testing-for-errors-in-swift-code)

## [Overview](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q\#overview)

If `condition` evaluates to `false`, an [`Issue`](https://developer.apple.com/documentation/testing/issue) is recorded for the test that is running in the current task and an instance of [`ExpectationFailedError`](https://developer.apple.com/documentation/testing/expectationfailederror) is thrown.

## [See Also](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q\#see-also)

### [Checking expectations](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-5l63q\#Checking-expectations)

[`macro expect(Bool, @autoclosure () -> Comment?, sourceLocation: SourceLocation)`](https://developer.apple.com/documentation/testing/expect(_:_:sourcelocation:))

Check that an expectation has passed after a condition has been evaluated.

[`macro require<T>(T?, @autoclosure () -> Comment?, sourceLocation: SourceLocation) -> T`](https://developer.apple.com/documentation/testing/require(_:_:sourcelocation:)-6w9oo)

Unwrap an optional value or, if it is `nil`, fail and throw an error.

Current page is require(\_:\_:sourceLocation:)

## Condition Trait Testing
[Skip Navigation](https://developer.apple.com/documentation/testing/conditiontrait/enabled(_:sourcelocation:_:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [ConditionTrait](https://developer.apple.com/documentation/testing/conditiontrait)
- enabled(\_:sourceLocation:\_:)

Type Method

# enabled(\_:sourceLocation:\_:)

Constructs a condition trait that disables a test if it returns `false`.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
static func enabled(
    _ comment: Comment? = nil,
    sourceLocation: SourceLocation = #_sourceLocation,
    _ condition: @escaping () async throws -> Bool
) -> Self
```

Available when `Self` is `ConditionTrait`.

## [Parameters](https://developer.apple.com/documentation/testing/conditiontrait/enabled(_:sourcelocation:_:)\#parameters)

`comment`

An optional comment that describes this trait.

`sourceLocation`

The source location of the trait.

`condition`

A closure that contains the trait’s custom condition logic. If this closure returns `true`, the trait allows the test to run. Otherwise, the testing library skips the test.

## [Return Value](https://developer.apple.com/documentation/testing/conditiontrait/enabled(_:sourcelocation:_:)\#return-value)

An instance of [`ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait) that evaluates the closure you provide.

Current page is enabled(\_:sourceLocation:\_:)

## Known Issue Invocation
[Skip Navigation](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:when:matching:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- withKnownIssue(\_:isIntermittent:sourceLocation:\_:when:matching:)

Function

# withKnownIssue(\_:isIntermittent:sourceLocation:\_:when:matching:)

Invoke a function that has a known issue that is expected to occur during its execution.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
func withKnownIssue(
    _ comment: Comment? = nil,
    isIntermittent: Bool = false,
    sourceLocation: SourceLocation = #_sourceLocation,
    _ body: () throws -> Void,
    when precondition: () -> Bool = { true },
    matching issueMatcher: @escaping KnownIssueMatcher = { _ in true }
) rethrows
```

## [Parameters](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:when:matching:)\#parameters)

`comment`

An optional comment describing the known issue.

`isIntermittent`

Whether or not the known issue occurs intermittently. If this argument is `true` and the known issue does not occur, no secondary issue is recorded.

`sourceLocation`

The source location to which any recorded issues should be attributed.

`body`

The function to invoke.

`precondition`

A function that determines if issues are known to occur during the execution of `body`. If this function returns `true`, encountered issues that are matched by `issueMatcher` are considered to be known issues; if this function returns `false`, `issueMatcher` is not called and they are treated as unknown.

`issueMatcher`

A function to invoke when an issue occurs that is used to determine if the issue is known to occur. By default, all issues match.

## [Mentioned in](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:when:matching:)\#mentions)

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

## [Discussion](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:when:matching:)\#discussion)

Use this function when a test is known to raise one or more issues that should not cause the test to fail, or if a precondition affects whether issues are known to occur. For example:

