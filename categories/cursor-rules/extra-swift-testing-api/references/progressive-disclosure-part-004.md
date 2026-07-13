```
@Test func example() throws {
  try withKnownIssue {
    try flakyCall()
  } when: {
    callsAreFlakyOnThisPlatform()
  } matching: { issue in
    issue.error is FileNotFoundError
  }
}

```

It is not necessary to specify both `precondition` and `issueMatcher` if only one is relevant. If all errors and issues should be considered known issues, use [`withKnownIssue(_:isIntermittent:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:)) instead.

## [See Also](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:when:matching:)\#see-also)

### [Recording known issues in tests](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:when:matching:)\#Recording-known-issues-in-tests)

[`func withKnownIssue(Comment?, isIntermittent: Bool, sourceLocation: SourceLocation, () throws -> Void)`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:sourcelocation:_:))

Invoke a function that has a known issue that is expected to occur during its execution.

[`func withKnownIssue(Comment?, isIntermittent: Bool, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, () async throws -> Void) async`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:isolation:sourcelocation:_:))

Invoke a function that has a known issue that is expected to occur during its execution.

[`func withKnownIssue(Comment?, isIntermittent: Bool, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, () async throws -> Void, when: () async -> Bool, matching: KnownIssueMatcher) async rethrows`](https://developer.apple.com/documentation/testing/withknownissue(_:isintermittent:isolation:sourcelocation:_:when:matching:))

Invoke a function that has a known issue that is expected to occur during its execution.

[`typealias KnownIssueMatcher`](https://developer.apple.com/documentation/testing/knownissuematcher)

A function that is used to match known issues.

Current page is withKnownIssue(\_:isIntermittent:sourceLocation:\_:when:matching:)

## Parameterized Testing in Swift
[Skip Navigation](https://developer.apple.com/documentation/testing/test(_:_:arguments:_:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Test(\_:\_:arguments:\_:)

Macro

# Test(\_:\_:arguments:\_:)

Declare a test parameterized over two collections of values.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
@attached(peer)
macro Test<C1, C2>(
    _ displayName: String? = nil,
    _ traits: any TestTrait...,
    arguments collection1: C1,
    _ collection2: C2
) where C1 : Collection, C1 : Sendable, C2 : Collection, C2 : Sendable, C1.Element : Sendable, C2.Element : Sendable
```

## [Parameters](https://developer.apple.com/documentation/testing/test(_:_:arguments:_:)\#parameters)

`displayName`

The customized display name of this test. If the value of this argument is `nil`, the display name of the test is derived from the associated function’s name.

`traits`

Zero or more traits to apply to this test.

`collection1`

A collection of values to pass to `testFunction`.

`collection2`

A second collection of values to pass to `testFunction`.

## [Overview](https://developer.apple.com/documentation/testing/test(_:_:arguments:_:)\#overview)

During testing, the associated test function is called once for each pair of elements in `collection1` and `collection2`.

## [See Also](https://developer.apple.com/documentation/testing/test(_:_:arguments:_:)\#see-also)

### [Related Documentation](https://developer.apple.com/documentation/testing/test(_:_:arguments:_:)\#Related-Documentation)

[Defining test functions](https://developer.apple.com/documentation/testing/definingtests)

Define a test function to validate that code is working correctly.

### [Test parameterization](https://developer.apple.com/documentation/testing/test(_:_:arguments:_:)\#Test-parameterization)

[Implementing parameterized tests](https://developer.apple.com/documentation/testing/parameterizedtesting)

Specify different input parameters to generate multiple test cases from a test function.

[`macro Test<C>(String?, any TestTrait..., arguments: C)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-8kn7a)

Declare a test parameterized over a collection of values.

[`macro Test<C1, C2>(String?, any TestTrait..., arguments: Zip2Sequence<C1, C2>)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok)

Declare a test parameterized over two zipped collections of values.

[`protocol CustomTestArgumentEncodable`](https://developer.apple.com/documentation/testing/customtestargumentencodable)

A protocol for customizing how arguments passed to parameterized tests are encoded, which is used to match against when running specific arguments.

[`struct Case`](https://developer.apple.com/documentation/testing/test/case)

A single test case from a parameterized [`Test`](https://developer.apple.com/documentation/testing/test).

Current page is Test(\_:\_:arguments:\_:)

## Test Declaration Macro
[Skip Navigation](https://developer.apple.com/documentation/testing/test(_:_:)#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Test(\_:\_:)

Macro

# Test(\_:\_:)

Declare a test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
@attached(peer)
macro Test(
    _ displayName: String? = nil,
    _ traits: any TestTrait...
)
```

## [Parameters](https://developer.apple.com/documentation/testing/test(_:_:)\#parameters)

`displayName`

The customized display name of this test. If the value of this argument is `nil`, the display name of the test is derived from the associated function’s name.

`traits`

Zero or more traits to apply to this test.

## [See Also](https://developer.apple.com/documentation/testing/test(_:_:)\#see-also)

### [Related Documentation](https://developer.apple.com/documentation/testing/test(_:_:)\#Related-Documentation)

[Defining test functions](https://developer.apple.com/documentation/testing/definingtests)

Define a test function to validate that code is working correctly.

### [Essentials](https://developer.apple.com/documentation/testing/test(_:_:)\#Essentials)

[Defining test functions](https://developer.apple.com/documentation/testing/definingtests)

Define a test function to validate that code is working correctly.

[Organizing test functions with suite types](https://developer.apple.com/documentation/testing/organizingtests)

Organize tests into test suites.

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

Migrate an existing test method or test class written using XCTest.

[`struct Test`](https://developer.apple.com/documentation/testing/test)

A type representing a test or suite.

[`macro Suite(String?, any SuiteTrait...)`](https://developer.apple.com/documentation/testing/suite(_:_:))

Declare a test suite.

Current page is Test(\_:\_:)