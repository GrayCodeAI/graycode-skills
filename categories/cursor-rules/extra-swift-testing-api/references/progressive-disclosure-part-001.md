
# https://developer.apple.com/documentation/testing llms-full.txt

## Swift Testing Overview
[Skip Navigation](https://developer.apple.com/documentation/testing#app-main)

Framework

# Swift Testing

Create and run tests for your Swift packages and Xcode projects.

Swift 6.0+Xcode 16.0+

## [Overview](https://developer.apple.com/documentation/testing\#Overview)

![The Swift logo on a blue gradient background that contains function, number, tag, and checkmark diamond symbols.](https://docs-assets.developer.apple.com/published/bb0ec39fe3198b15d431887aac09a527/swift-testing-hero%402x.png)

With Swift Testing you leverage powerful and expressive capabilities of the Swift programming language to develop tests with more confidence and less code. The library integrates seamlessly with Swift Package Manager testing workflow, supports flexible test organization, customizable metadata, and scalable test execution.

- Define test functions almost anywhere with a single attribute.

- Group related tests into hierarchies using Swift’s type system.

- Integrate seamlessly with Swift concurrency.

- Parameterize test functions across wide ranges of inputs.

- Enable tests dynamically depending on runtime conditions.

- Parallelize tests in-process.

- Categorize tests using tags.

- Associate bugs directly with the tests that verify their fixes or reproduce their problems.


#### [Related videos](https://developer.apple.com/documentation/testing\#Related-videos)

[![](https://devimages-cdn.apple.com/wwdc-services/images/C03E6E6D-A32A-41D0-9E50-C3C6059820AA/E94A25C1-8734-483C-A4C1-862533C307AC/9309_wide_250x141_3x.jpg)\\
\\
Meet Swift Testing](https://developer.apple.com/videos/play/wwdc2024/10179)

[![](https://devimages-cdn.apple.com/wwdc-services/images/C03E6E6D-A32A-41D0-9E50-C3C6059820AA/52DB5AB3-48AF-40E1-98C7-CCC9132EDD39/9325_wide_250x141_3x.jpg)\\
\\
Go further with Swift Testing](https://developer.apple.com/videos/play/wwdc2024/10195)

## [Topics](https://developer.apple.com/documentation/testing\#topics)

### [Essentials](https://developer.apple.com/documentation/testing\#Essentials)

[Defining test functions](https://developer.apple.com/documentation/testing/definingtests)

Define a test function to validate that code is working correctly.

[Organizing test functions with suite types](https://developer.apple.com/documentation/testing/organizingtests)

Organize tests into test suites.

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

Migrate an existing test method or test class written using XCTest.

[`macro Test(String?, any TestTrait...)`](https://developer.apple.com/documentation/testing/test(_:_:))

Declare a test.

[`struct Test`](https://developer.apple.com/documentation/testing/test)

A type representing a test or suite.

[`macro Suite(String?, any SuiteTrait...)`](https://developer.apple.com/documentation/testing/suite(_:_:))

Declare a test suite.

### [Test parameterization](https://developer.apple.com/documentation/testing\#Test-parameterization)

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

[`struct Case`](https://developer.apple.com/documentation/testing/test/case)

A single test case from a parameterized [`Test`](https://developer.apple.com/documentation/testing/test).

### [Behavior validation](https://developer.apple.com/documentation/testing\#Behavior-validation)

[API Reference\\
Expectations and confirmations](https://developer.apple.com/documentation/testing/expectations)

Check for expected values, outcomes, and asynchronous events in tests.

[API Reference\\
Known issues](https://developer.apple.com/documentation/testing/known-issues)

Highlight known issues when running tests.

### [Test customization](https://developer.apple.com/documentation/testing\#Test-customization)

[API Reference\\
Traits](https://developer.apple.com/documentation/testing/traits)

Annotate test functions and suites, and customize their behavior.

Current page is Swift Testing

## Adding Tags to Tests
[Skip Navigation](https://developer.apple.com/documentation/testing/addingtags#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Traits](https://developer.apple.com/documentation/testing/traits)
- Adding tags to tests

Article

# Adding tags to tests

Use tags to provide semantic information for organization, filtering, and customizing appearances.

## [Overview](https://developer.apple.com/documentation/testing/addingtags\#Overview)

A complex package or project may contain hundreds or thousands of tests and suites. Some subset of those tests may share some common facet, such as being _critical_ or _flaky_. The testing library includes a type of trait called _tags_ that you can add to group and categorize tests.

Tags are different from test suites: test suites impose structure on test functions at the source level, while tags provide semantic information for a test that can be shared with any number of other tests across test suites, source files, and even test targets.

## [Add a tag](https://developer.apple.com/documentation/testing/addingtags\#Add-a-tag)

To add a tag to a test, use the [`tags(_:)`](https://developer.apple.com/documentation/testing/trait/tags(_:)) trait. This trait takes a sequence of tags as its argument, and those tags are then applied to the corresponding test at runtime. If any tags are applied to a test suite, then all tests in that suite inherit those tags.

The testing library doesn’t assign any semantic meaning to any tags, nor does the presence or absence of tags affect how the testing library runs tests.

Tags themselves are instances of [`Tag`](https://developer.apple.com/documentation/testing/tag) and expressed as named constants declared as static members of [`Tag`](https://developer.apple.com/documentation/testing/tag). To declare a named constant tag, use the [`Tag()`](https://developer.apple.com/documentation/testing/tag()) macro:

```
extension Tag {
  @Tag static var legallyRequired: Self
}

@Test("Vendor's license is valid", .tags(.legallyRequired))
func licenseValid() { ... }

```

If two tags with the same name ( `legallyRequired` in the above example) are declared in different files, modules, or other contexts, the testing library treats them as equivalent.

If it’s important for a tag to be distinguished from similar tags declared elsewhere in a package or project (or its dependencies), use reverse-DNS naming to create a unique Swift symbol name for your tag:

```
extension Tag {
  enum com_example_foodtruck {}
}

extension Tag.com_example_foodtruck {
  @Tag static var extraSpecial: Tag
}

@Test(
  "Extra Special Sauce recipe is secret",
  .tags(.com_example_foodtruck.extraSpecial)
)
func secretSauce() { ... }

```

### [Where tags can be declared](https://developer.apple.com/documentation/testing/addingtags\#Where-tags-can-be-declared)

Tags must always be declared as members of [`Tag`](https://developer.apple.com/documentation/testing/tag) in an extension to that type or in a type nested within [`Tag`](https://developer.apple.com/documentation/testing/tag). Redeclaring a tag under a second name has no effect and the additional name will not be recognized by the testing library. The following example is unsupported:

```
extension Tag {
  @Tag static var legallyRequired: Self // ✅ OK: Declaring a new tag.

  static var requiredByLaw: Self { // ❌ ERROR: This tag name isn't
                                   // recognized at runtime.
    legallyRequired
  }
}

```

If a tag is declared as a named constant outside of an extension to the [`Tag`](https://developer.apple.com/documentation/testing/tag) type (for example, at the root of a file or in another unrelated type declaration), it cannot be applied to test functions or test suites. The following declarations are unsupported:

```
@Tag let needsKetchup: Self // ❌ ERROR: Tags must be declared in an extension
                            // to Tag.
struct Food {
  @Tag var needsMustard: Self // ❌ ERROR: Tags must be declared in an extension
                              // to Tag.
}

```

## [See Also](https://developer.apple.com/documentation/testing/addingtags\#see-also)

### [Annotating tests](https://developer.apple.com/documentation/testing/addingtags\#Annotating-tests)

[Adding comments to tests](https://developer.apple.com/documentation/testing/addingcomments)

Add comments to provide useful information about tests.

[Associating bugs with tests](https://developer.apple.com/documentation/testing/associatingbugs)

Associate bugs uncovered or verified by tests.

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

Current page is Adding tags to tests

## Swift Test Overview
[Skip Navigation](https://developer.apple.com/documentation/testing/test#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Test

Structure

# Test

A type representing a test or suite.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct Test
```

## [Overview](https://developer.apple.com/documentation/testing/test\#overview)

An instance of this type may represent:

- A type containing zero or more tests (i.e. a _test suite_);

- An individual test function (possibly contained within a type); or

- A test function parameterized over one or more sequences of inputs.


Two instances of this type are considered to be equal if the values of their [`id`](https://developer.apple.com/documentation/testing/test/id-swift.property) properties are equal.

## [Topics](https://developer.apple.com/documentation/testing/test\#topics)

### [Structures](https://developer.apple.com/documentation/testing/test\#Structures)

[`struct Case`](https://developer.apple.com/documentation/testing/test/case)

A single test case from a parameterized [`Test`](https://developer.apple.com/documentation/testing/test).

### [Instance Properties](https://developer.apple.com/documentation/testing/test\#Instance-Properties)

[`var associatedBugs: [Bug]`](https://developer.apple.com/documentation/testing/test/associatedbugs)

The set of bugs associated with this test.

[`var comments: [Comment]`](https://developer.apple.com/documentation/testing/test/comments)

The complete set of comments about this test from all of its traits.

[`var displayName: String?`](https://developer.apple.com/documentation/testing/test/displayname)

The customized display name of this instance, if specified.

[`var isParameterized: Bool`](https://developer.apple.com/documentation/testing/test/isparameterized)

Whether or not this test is parameterized.

[`var isSuite: Bool`](https://developer.apple.com/documentation/testing/test/issuite)

Whether or not this instance is a test suite containing other tests.

[`var name: String`](https://developer.apple.com/documentation/testing/test/name)

The name of this instance.

[`var sourceLocation: SourceLocation`](https://developer.apple.com/documentation/testing/test/sourcelocation)

The source location of this test.

[`var tags: Set<Tag>`](https://developer.apple.com/documentation/testing/test/tags)

The complete, unique set of tags associated with this test.

[`var timeLimit: Duration?`](https://developer.apple.com/documentation/testing/test/timelimit)

The maximum amount of time this test’s cases may run for.

[`var traits: [any Trait]`](https://developer.apple.com/documentation/testing/test/traits)

The set of traits added to this instance when it was initialized.

### [Type Properties](https://developer.apple.com/documentation/testing/test\#Type-Properties)

[`static var current: Test?`](https://developer.apple.com/documentation/testing/test/current)

The test that is running on the current task, if any.

### [Default Implementations](https://developer.apple.com/documentation/testing/test\#Default-Implementations)

[API Reference\\
Equatable Implementations](https://developer.apple.com/documentation/testing/test/equatable-implementations)

[API Reference\\
Hashable Implementations](https://developer.apple.com/documentation/testing/test/hashable-implementations)

[API Reference\\
Identifiable Implementations](https://developer.apple.com/documentation/testing/test/identifiable-implementations)

## [Relationships](https://developer.apple.com/documentation/testing/test\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/test\#conforms-to)

- [`Copyable`](https://developer.apple.com/documentation/Swift/Copyable)
- [`Equatable`](https://developer.apple.com/documentation/Swift/Equatable)
- [`Hashable`](https://developer.apple.com/documentation/Swift/Hashable)
- [`Identifiable`](https://developer.apple.com/documentation/Swift/Identifiable)
- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)

## [See Also](https://developer.apple.com/documentation/testing/test\#see-also)

### [Essentials](https://developer.apple.com/documentation/testing/test\#Essentials)

[Defining test functions](https://developer.apple.com/documentation/testing/definingtests)

Define a test function to validate that code is working correctly.

[Organizing test functions with suite types](https://developer.apple.com/documentation/testing/organizingtests)

Organize tests into test suites.

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

Migrate an existing test method or test class written using XCTest.

[`macro Test(String?, any TestTrait...)`](https://developer.apple.com/documentation/testing/test(_:_:))

Declare a test.

[`macro Suite(String?, any SuiteTrait...)`](https://developer.apple.com/documentation/testing/suite(_:_:))

Declare a test suite.

Current page is Test

## Adding Comments to Tests
[Skip Navigation](https://developer.apple.com/documentation/testing/addingcomments#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Traits](https://developer.apple.com/documentation/testing/traits)
- Adding comments to tests

Article

# Adding comments to tests

Add comments to provide useful information about tests.

## [Overview](https://developer.apple.com/documentation/testing/addingcomments\#Overview)

It’s often useful to add comments to code to:

- Provide context or background information about the code’s purpose

- Explain how complex code implemented

- Include details which may be helpful when diagnosing issues


Test code is no different and can benefit from explanatory code comments, but often test issues are shown in places where the source code of the test is unavailable such as in continuous integration (CI) interfaces or in log files.

Seeing comments related to tests in these contexts can help diagnose issues more quickly. Comments can be added to test declarations and the testing library will automatically capture and show them when issues are recorded.

## [Add a code comment to a test](https://developer.apple.com/documentation/testing/addingcomments\#Add-a-code-comment-to-a-test)

To include a comment on a test or suite, write an ordinary Swift code comment immediately before its `@Test` or `@Suite` attribute:

```
// Assumes the standard lunch menu includes a taco
@Test func lunchMenu() {
  let foodTruck = FoodTruck(
    menu: .lunch,
    ingredients: [.tortillas, .cheese]
  )
  #expect(foodTruck.menu.contains { $0 is Taco })
}

```

The comment, `// Assumes the standard lunch menu includes a taco`, is added to the test.

The following language comment styles are supported:

| Syntax | Style |
| --- | --- |
| `// ...` | Line comment |
| `/// ...` | Documentation line comment |
| `/* ... */` | Block comment |
| `/** ... */` | Documentation block comment |

### [Comment formatting](https://developer.apple.com/documentation/testing/addingcomments\#Comment-formatting)

Test comments which are automatically added from source code comments preserve their original formatting, including any prefixes like `//` or `/**`. This is because the whitespace and formatting of comments can be meaningful in some circumstances or aid in understanding the comment — for example, when a comment includes an example code snippet or diagram.

## [Use test comments effectively](https://developer.apple.com/documentation/testing/addingcomments\#Use-test-comments-effectively)

As in normal code, comments on tests are generally most useful when they:

- Add information that isn’t obvious from reading the code

- Provide useful information about the operation or motivation of a test


If a test is related to a bug or issue, consider using the [`Bug`](https://developer.apple.com/documentation/testing/bug) trait instead of comments. For more information, see [Associating bugs with tests](https://developer.apple.com/documentation/testing/associatingbugs).

## [See Also](https://developer.apple.com/documentation/testing/addingcomments\#see-also)

### [Annotating tests](https://developer.apple.com/documentation/testing/addingcomments\#Annotating-tests)

[Adding tags to tests](https://developer.apple.com/documentation/testing/addingtags)

Use tags to provide semantic information for organization, filtering, and customizing appearances.

[Associating bugs with tests](https://developer.apple.com/documentation/testing/associatingbugs)

Associate bugs uncovered or verified by tests.

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

Current page is Adding comments to tests

## Organizing Test Functions
[Skip Navigation](https://developer.apple.com/documentation/testing/organizingtests#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Organizing test functions with suite types

Article

# Organizing test functions with suite types

Organize tests into test suites.

## [Overview](https://developer.apple.com/documentation/testing/organizingtests\#Overview)

When working with a large selection of test functions, it can be helpful to organize them into test suites.

A test function can be added to a test suite in one of two ways:

- By placing it in a Swift type.

- By placing it in a Swift type and annotating that type with the `@Suite` attribute.


The `@Suite` attribute isn’t required for the testing library to recognize that a type contains test functions, but adding it allows customization of a test suite’s appearance in the IDE and at the command line. If a trait such as [`tags(_:)`](https://developer.apple.com/documentation/testing/trait/tags(_:)) or [`disabled(_:sourceLocation:)`](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:)) is applied to a test suite, it’s automatically inherited by the tests contained in the suite.

In addition to containing test functions and any other members that a Swift type might contain, test suite types can also contain additional test suites nested within them. To add a nested test suite type, simply declare an additional type within the scope of the outer test suite type.

By default, tests contained within a suite run in parallel with each other. For more information about test parallelization, see [Running tests serially or in parallel](https://developer.apple.com/documentation/testing/parallelization).

### [Customize a suite’s name](https://developer.apple.com/documentation/testing/organizingtests\#Customize-a-suites-name)

To customize a test suite’s name, supply a string literal as an argument to the `@Suite` attribute:

```
@Suite("Food truck tests") struct FoodTruckTests {
  @Test func foodTruckExists() { ... }
}

```

To further customize the appearance and behavior of a test function, use [traits](https://developer.apple.com/documentation/testing/traits) such as [`tags(_:)`](https://developer.apple.com/documentation/testing/trait/tags(_:)).

## [Test functions in test suite types](https://developer.apple.com/documentation/testing/organizingtests\#Test-functions-in-test-suite-types)

If a type contains a test function declared as an instance method (that is, without either the `static` or `class` keyword), the testing library calls that test function at runtime by initializing an instance of the type, then calling the test function on that instance. If a test suite type contains multiple test functions declared as instance methods, each one is called on a distinct instance of the type. Therefore, the following test suite and test function:

```
@Suite struct FoodTruckTests {
  @Test func foodTruckExists() { ... }
}

```

Are equivalent to:

```
@Suite struct FoodTruckTests {
  func foodTruckExists() { ... }

  @Test static func staticFoodTruckExists() {
    let instance = FoodTruckTests()
    instance.foodTruckExists()
  }
}

```

### [Constraints on test suite types](https://developer.apple.com/documentation/testing/organizingtests\#Constraints-on-test-suite-types)

When using a type as a test suite, it’s subject to some constraints that are not otherwise applied to Swift types.

#### [An initializer may be required](https://developer.apple.com/documentation/testing/organizingtests\#An-initializer-may-be-required)

If a type contains test functions declared as instance methods, it must be possible to initialize an instance of the type with a zero-argument initializer. The initializer may be any combination of:

- implicit or explicit

- synchronous or asynchronous

- throwing or non-throwing

- `private`, `fileprivate`, `internal`, `package`, or `public`


For example:

```
@Suite struct FoodTruckTests {
  var batteryLevel = 100

  @Test func foodTruckExists() { ... } // ✅ OK: The type has an implicit init().
}

@Suite struct CashRegisterTests {
  private init(cashOnHand: Decimal = 0.0) async throws { ... }

  @Test func calculateSalesTax() { ... } // ✅ OK: The type has a callable init().
}

struct MenuTests {
  var foods: [Food]
  var prices: [Food: Decimal]

  @Test static func specialOfTheDay() { ... } // ✅ OK: The function is static.
  @Test func orderAllFoods() { ... } // ❌ ERROR: The suite type requires init().
}

```

The compiler emits an error when presented with a test suite that doesn’t meet this requirement.

### [Test suite types must always be available](https://developer.apple.com/documentation/testing/organizingtests\#Test-suite-types-must-always-be-available)

Although `@available` can be applied to a test function to limit its availability at runtime, a test suite type (and any types that contain it) must _not_ be annotated with the `@available` attribute:

```
@Suite struct FoodTruckTests { ... } // ✅ OK: The type is always available.

@available(macOS 11.0, *) // ❌ ERROR: The suite type must always be available.
@Suite struct CashRegisterTests { ... }

@available(macOS 11.0, *) struct MenuItemTests { // ❌ ERROR: The suite type's
                                                 // containing type must always
                                                 // be available too.
  @Suite struct BurgerTests { ... }
}

```

The compiler emits an error when presented with a test suite that doesn’t meet this requirement.

## [See Also](https://developer.apple.com/documentation/testing/organizingtests\#see-also)

### [Essentials](https://developer.apple.com/documentation/testing/organizingtests\#Essentials)

[Defining test functions](https://developer.apple.com/documentation/testing/definingtests)

Define a test function to validate that code is working correctly.

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

Migrate an existing test method or test class written using XCTest.

[`macro Test(String?, any TestTrait...)`](https://developer.apple.com/documentation/testing/test(_:_:))

Declare a test.

[`struct Test`](https://developer.apple.com/documentation/testing/test)

A type representing a test or suite.

[`macro Suite(String?, any SuiteTrait...)`](https://developer.apple.com/documentation/testing/suite(_:_:))

Declare a test suite.

Current page is Organizing test functions with suite types

## Custom Test Argument Encoding
[Skip Navigation](https://developer.apple.com/documentation/testing/customtestargumentencodable#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- CustomTestArgumentEncodable

Protocol

# CustomTestArgumentEncodable

A protocol for customizing how arguments passed to parameterized tests are encoded, which is used to match against when running specific arguments.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
protocol CustomTestArgumentEncodable : Sendable
```

## [Mentioned in](https://developer.apple.com/documentation/testing/customtestargumentencodable\#mentions)

[Implementing parameterized tests](https://developer.apple.com/documentation/testing/parameterizedtesting)

## [Overview](https://developer.apple.com/documentation/testing/customtestargumentencodable\#overview)

The testing library checks whether a test argument conforms to this protocol, or any of several other known protocols, when running selected test cases. When a test argument conforms to this protocol, that conformance takes highest priority, and the testing library will then call [`encodeTestArgument(to:)`](https://developer.apple.com/documentation/testing/customtestargumentencodable/encodetestargument(to:)) on the argument. A type that conforms to this protocol is not required to conform to either `Encodable` or `Decodable`.

See [Implementing parameterized tests](https://developer.apple.com/documentation/testing/parameterizedtesting) for a list of the other supported ways to allow running selected test cases.

## [Topics](https://developer.apple.com/documentation/testing/customtestargumentencodable\#topics)

### [Instance Methods](https://developer.apple.com/documentation/testing/customtestargumentencodable\#Instance-Methods)

[`func encodeTestArgument(to: some Encoder) throws`](https://developer.apple.com/documentation/testing/customtestargumentencodable/encodetestargument(to:))

Encode this test argument.

**Required**

## [Relationships](https://developer.apple.com/documentation/testing/customtestargumentencodable\#relationships)

### [Inherits From](https://developer.apple.com/documentation/testing/customtestargumentencodable\#inherits-from)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)

## [See Also](https://developer.apple.com/documentation/testing/customtestargumentencodable\#see-also)

### [Related Documentation](https://developer.apple.com/documentation/testing/customtestargumentencodable\#Related-Documentation)

[Implementing parameterized tests](https://developer.apple.com/documentation/testing/parameterizedtesting)

Specify different input parameters to generate multiple test cases from a test function.

### [Test parameterization](https://developer.apple.com/documentation/testing/customtestargumentencodable\#Test-parameterization)

[Implementing parameterized tests](https://developer.apple.com/documentation/testing/parameterizedtesting)

Specify different input parameters to generate multiple test cases from a test function.

[`macro Test<C>(String?, any TestTrait..., arguments: C)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-8kn7a)

Declare a test parameterized over a collection of values.

[`macro Test<C1, C2>(String?, any TestTrait..., arguments: C1, C2)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:_:))

Declare a test parameterized over two collections of values.

[`macro Test<C1, C2>(String?, any TestTrait..., arguments: Zip2Sequence<C1, C2>)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok)

Declare a test parameterized over two zipped collections of values.

[`struct Case`](https://developer.apple.com/documentation/testing/test/case)

A single test case from a parameterized [`Test`](https://developer.apple.com/documentation/testing/test).

Current page is CustomTestArgumentEncodable

## Defining Test Functions
[Skip Navigation](https://developer.apple.com/documentation/testing/definingtests#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Defining test functions

Article

# Defining test functions

Define a test function to validate that code is working correctly.

## [Overview](https://developer.apple.com/documentation/testing/definingtests\#Overview)

Defining a test function for a Swift package or project is straightforward.

### [Import the testing library](https://developer.apple.com/documentation/testing/definingtests\#Import-the-testing-library)

To import the testing library, add the following to the Swift source file that contains the test:

```
import Testing

```

### [Declare a test function](https://developer.apple.com/documentation/testing/definingtests\#Declare-a-test-function)

To declare a test function, write a Swift function declaration that doesn’t take any arguments, then prefix its name with the `@Test` attribute:

```
@Test func foodTruckExists() {
  // Test logic goes here.
}

```

This test function can be present at file scope or within a type. A type containing test functions is automatically a _test suite_ and can be optionally annotated with the `@Suite` attribute. For more information about suites, see [Organizing test functions with suite types](https://developer.apple.com/documentation/testing/organizingtests).

Note that, while this function is a valid test function, it doesn’t actually perform any action or test any code. To check for expected values and outcomes in test functions, add [expectations](https://developer.apple.com/documentation/testing/expectations) to the test function.

### [Customize a test’s name](https://developer.apple.com/documentation/testing/definingtests\#Customize-a-tests-name)

To customize a test function’s name as presented in an IDE or at the command line, supply a string literal as an argument to the `@Test` attribute:

```
@Test("Food truck exists") func foodTruckExists() { ... }

```

To further customize the appearance and behavior of a test function, use [traits](https://developer.apple.com/documentation/testing/traits) such as [`tags(_:)`](https://developer.apple.com/documentation/testing/trait/tags(_:)).

### [Write concurrent or throwing tests](https://developer.apple.com/documentation/testing/definingtests\#Write-concurrent-or-throwing-tests)

As with other Swift functions, test functions can be marked `async` and `throws` to annotate them as concurrent or throwing, respectively. If a test is only safe to run in the main actor’s execution context (that is, from the main thread of the process), it can be annotated `@MainActor`:

```
@Test @MainActor func foodTruckExists() async throws { ... }

```

### [Limit the availability of a test](https://developer.apple.com/documentation/testing/definingtests\#Limit-the-availability-of-a-test)

If a test function can only run on newer versions of an operating system or of the Swift language, use the `@available` attribute when declaring it. Use the `message` argument of the `@available` attribute to specify a message to log if a test is unable to run due to limited availability:

```
@available(macOS 11.0, *)
@available(swift, introduced: 8.0, message: "Requires Swift 8.0 features to run")
@Test func foodTruckExists() { ... }

```

## [See Also](https://developer.apple.com/documentation/testing/definingtests\#see-also)

### [Essentials](https://developer.apple.com/documentation/testing/definingtests\#Essentials)

[Organizing test functions with suite types](https://developer.apple.com/documentation/testing/organizingtests)

Organize tests into test suites.

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

Migrate an existing test method or test class written using XCTest.

[`macro Test(String?, any TestTrait...)`](https://developer.apple.com/documentation/testing/test(_:_:))

Declare a test.

[`struct Test`](https://developer.apple.com/documentation/testing/test)

A type representing a test or suite.

[`macro Suite(String?, any SuiteTrait...)`](https://developer.apple.com/documentation/testing/suite(_:_:))

Declare a test suite.

Current page is Defining test functions

## Interpreting Bug Identifiers
[Skip Navigation](https://developer.apple.com/documentation/testing/bugidentifiers#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Traits](https://developer.apple.com/documentation/testing/traits)
- Interpreting bug identifiers

Article

# Interpreting bug identifiers

Examine how the testing library interprets bug identifiers provided by developers.

## [Overview](https://developer.apple.com/documentation/testing/bugidentifiers\#Overview)

The testing library supports two distinct ways to identify a bug:

1. A URL linking to more information about the bug; and

2. A unique identifier in the bug’s associated bug-tracking system.


A bug may have both an associated URL _and_ an associated unique identifier. It must have at least one or the other in order for the testing library to be able to interpret it correctly.

To create an instance of [`Bug`](https://developer.apple.com/documentation/testing/bug) with a URL, use the [`bug(_:_:)`](https://developer.apple.com/documentation/testing/trait/bug(_:_:)) trait. At compile time, the testing library will validate that the given string can be parsed as a URL according to [RFC 3986](https://www.ietf.org/rfc/rfc3986.txt).

To create an instance of [`Bug`](https://developer.apple.com/documentation/testing/bug) with a bug’s unique identifier, use the [`bug(_:id:_:)`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-10yf5) trait. The testing library does not require that a bug’s unique identifier match any particular format, but will interpret unique identifiers starting with `"FB"` as referring to bugs tracked with the [Apple Feedback Assistant](https://feedbackassistant.apple.com/). For convenience, you can also directly pass an integer as a bug’s identifier using [`bug(_:id:_:)`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-3vtpl).

### [Examples](https://developer.apple.com/documentation/testing/bugidentifiers\#Examples)

| Trait Function | Inferred Bug-Tracking System |
| --- | --- |
| `.bug(id: 12345)` | None |
| `.bug(id: "12345")` | None |
| `.bug("https://www.example.com?id=12345", id: "12345")` | None |
| `.bug("https://github.com/swiftlang/swift/pull/12345")` | [GitHub Issues for the Swift project](https://github.com/swiftlang/swift/issues) |
| `.bug("https://bugs.webkit.org/show_bug.cgi?id=12345")` | [WebKit Bugzilla](https://bugs.webkit.org/) |
| `.bug(id: "FB12345")` | Apple Feedback Assistant |

## [See Also](https://developer.apple.com/documentation/testing/bugidentifiers\#see-also)

### [Annotating tests](https://developer.apple.com/documentation/testing/bugidentifiers\#Annotating-tests)

[Adding tags to tests](https://developer.apple.com/documentation/testing/addingtags)

Use tags to provide semantic information for organization, filtering, and customizing appearances.

[Adding comments to tests](https://developer.apple.com/documentation/testing/addingcomments)

Add comments to provide useful information about tests.

[Associating bugs with tests](https://developer.apple.com/documentation/testing/associatingbugs)

Associate bugs uncovered or verified by tests.

[`macro Tag()`](https://developer.apple.com/documentation/testing/tag())

Declare a tag that can be applied to a test function or test suite.

[`static func bug(String, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:_:))

Constructs a bug to track with a test.

[`static func bug(String?, id: String, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-10yf5)

Constructs a bug to track with a test.

[`static func bug(String?, id: some Numeric, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-3vtpl)

Constructs a bug to track with a test.

Current page is Interpreting bug identifiers

## Limiting Test Execution Time
[Skip Navigation](https://developer.apple.com/documentation/testing/limitingexecutiontime#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- [Traits](https://developer.apple.com/documentation/testing/traits)
- Limiting the running time of tests

Article

# Limiting the running time of tests

Set limits on how long a test can run for until it fails.

## [Overview](https://developer.apple.com/documentation/testing/limitingexecutiontime\#Overview)

Some tests may naturally run slowly: they may require significant system resources to complete, may rely on downloaded data from a server, or may otherwise be dependent on external factors.

If a test may hang indefinitely or may consume too many system resources to complete effectively, consider setting a time limit for it so that it’s marked as failing if it runs for an excessive amount of time. Use the [`timeLimit(_:)`](https://developer.apple.com/documentation/testing/trait/timelimit(_:)) trait as an upper bound:

```
@Test(.timeLimit(.minutes(60))
func serve100CustomersInOneHour() async {
  for _ in 0 ..< 100 {
    let customer = await Customer.next()
    await customer.order()
    ...
  }
}

```

If the above test function takes longer than an hour (60 x 60 seconds) to execute, the task in which it’s running is [cancelled](https://developer.apple.com/documentation/swift/task/cancel()) and the test fails with an issue of kind [`Issue.Kind.timeLimitExceeded(timeLimitComponents:)`](https://developer.apple.com/documentation/testing/issue/kind-swift.enum/timelimitexceeded(timelimitcomponents:)).

The testing library may adjust the specified time limit for performance reasons or to ensure tests have enough time to run. In particular, a granularity of (by default) one minute is applied to tests. The testing library can also be configured with a maximum time limit per test that overrides any applied time limit traits.

### [Time limits applied to test suites](https://developer.apple.com/documentation/testing/limitingexecutiontime\#Time-limits-applied-to-test-suites)

When a time limit is applied to a test suite, it’s recursively applied to all test functions and child test suites within that suite.

### [Time limits applied to parameterized tests](https://developer.apple.com/documentation/testing/limitingexecutiontime\#Time-limits-applied-to-parameterized-tests)

When a time limit is applied to a parameterized test function, it’s applied to each invocation _separately_ so that if only some arguments cause failures, then successful arguments aren’t incorrectly marked as failing too.

## [See Also](https://developer.apple.com/documentation/testing/limitingexecutiontime\#see-also)

### [Customizing runtime behaviors](https://developer.apple.com/documentation/testing/limitingexecutiontime\#Customizing-runtime-behaviors)

[Enabling and disabling tests](https://developer.apple.com/documentation/testing/enablinganddisabling)

Conditionally enable or disable individual tests before they run.

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

Current page is Limiting the running time of tests

## Test Scoping Protocol
[Skip Navigation](https://developer.apple.com/documentation/testing/testscoping#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- TestScoping

Protocol

# TestScoping

A protocol that tells the test runner to run custom code before or after it runs a test suite or test function.

Swift 6.1+Xcode 16.3+

```
protocol TestScoping : Sendable
```

## [Overview](https://developer.apple.com/documentation/testing/testscoping\#overview)

Provide custom scope for tests by implementing the [`scopeProvider(for:testCase:)`](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:)) method, returning a type that conforms to this protocol. Create a custom scope to consolidate common set-up and tear-down logic for tests which have similar needs, which allows each test function to focus on the unique aspects of its test.

## [Topics](https://developer.apple.com/documentation/testing/testscoping\#topics)

### [Instance Methods](https://developer.apple.com/documentation/testing/testscoping\#Instance-Methods)

[`func provideScope(for: Test, testCase: Test.Case?, performing: () async throws -> Void) async throws`](https://developer.apple.com/documentation/testing/testscoping/providescope(for:testcase:performing:))

Provide custom execution scope for a function call which is related to the specified test or test case.

**Required**

## [Relationships](https://developer.apple.com/documentation/testing/testscoping\#relationships)

### [Inherits From](https://developer.apple.com/documentation/testing/testscoping\#inherits-from)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)

## [See Also](https://developer.apple.com/documentation/testing/testscoping\#see-also)

### [Creating custom traits](https://developer.apple.com/documentation/testing/testscoping\#Creating-custom-traits)

[`protocol Trait`](https://developer.apple.com/documentation/testing/trait)

A protocol describing traits that can be added to a test function or to a test suite.

[`protocol TestTrait`](https://developer.apple.com/documentation/testing/testtrait)

A protocol describing a trait that you can add to a test function.

[`protocol SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait)

A protocol describing a trait that you can add to a test suite.

Current page is TestScoping

## Event Confirmation Type
[Skip Navigation](https://developer.apple.com/documentation/testing/confirmation#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Confirmation

Structure

# Confirmation

A type that can be used to confirm that an event occurs zero or more times.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct Confirmation
```

## [Mentioned in](https://developer.apple.com/documentation/testing/confirmation\#mentions)

[Testing asynchronous code](https://developer.apple.com/documentation/testing/testing-asynchronous-code)

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

## [Topics](https://developer.apple.com/documentation/testing/confirmation\#topics)

### [Instance Methods](https://developer.apple.com/documentation/testing/confirmation\#Instance-Methods)

[`func callAsFunction(count: Int)`](https://developer.apple.com/documentation/testing/confirmation/callasfunction(count:))

Confirm this confirmation.

[`func confirm(count: Int)`](https://developer.apple.com/documentation/testing/confirmation/confirm(count:))

Confirm this confirmation.

## [Relationships](https://developer.apple.com/documentation/testing/confirmation\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/confirmation\#conforms-to)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)

## [See Also](https://developer.apple.com/documentation/testing/confirmation\#see-also)

### [Confirming that asynchronous events occur](https://developer.apple.com/documentation/testing/confirmation\#Confirming-that-asynchronous-events-occur)

[Testing asynchronous code](https://developer.apple.com/documentation/testing/testing-asynchronous-code)

Validate whether your code causes expected events to happen.

[`func confirmation<R>(Comment?, expectedCount: Int, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, (Confirmation) async throws -> sending R) async rethrows -> R`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-5mqz2)

Confirm that some event occurs during the invocation of a function.

[`func confirmation<R>(Comment?, expectedCount: some RangeExpression<Int> & Sendable & Sequence<Int>, isolation: isolated (any Actor)?, sourceLocation: SourceLocation, (Confirmation) async throws -> sending R) async rethrows -> R`](https://developer.apple.com/documentation/testing/confirmation(_:expectedcount:isolation:sourcelocation:_:)-l3il)

Confirm that some event occurs during the invocation of a function.

Current page is Confirmation

## Tag Type Overview
[Skip Navigation](https://developer.apple.com/documentation/testing/tag#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Tag

Structure

# Tag

A type representing a tag that can be applied to a test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct Tag
```

## [Mentioned in](https://developer.apple.com/documentation/testing/tag\#mentions)

[Adding tags to tests](https://developer.apple.com/documentation/testing/addingtags)

## [Overview](https://developer.apple.com/documentation/testing/tag\#overview)

To apply tags to a test, use the [`tags(_:)`](https://developer.apple.com/documentation/testing/trait/tags(_:)) function.

## [Topics](https://developer.apple.com/documentation/testing/tag\#topics)

### [Structures](https://developer.apple.com/documentation/testing/tag\#Structures)

[`struct List`](https://developer.apple.com/documentation/testing/tag/list)

A type representing one or more tags applied to a test.

### [Default Implementations](https://developer.apple.com/documentation/testing/tag\#Default-Implementations)

[API Reference\\
CodingKeyRepresentable Implementations](https://developer.apple.com/documentation/testing/tag/codingkeyrepresentable-implementations)

[API Reference\\
Comparable Implementations](https://developer.apple.com/documentation/testing/tag/comparable-implementations)

[API Reference\\
CustomStringConvertible Implementations](https://developer.apple.com/documentation/testing/tag/customstringconvertible-implementations)

[API Reference\\
Decodable Implementations](https://developer.apple.com/documentation/testing/tag/decodable-implementations)

[API Reference\\
Encodable Implementations](https://developer.apple.com/documentation/testing/tag/encodable-implementations)

[API Reference\\
Equatable Implementations](https://developer.apple.com/documentation/testing/tag/equatable-implementations)

[API Reference\\
Hashable Implementations](https://developer.apple.com/documentation/testing/tag/hashable-implementations)

## [Relationships](https://developer.apple.com/documentation/testing/tag\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/tag\#conforms-to)

- [`CodingKeyRepresentable`](https://developer.apple.com/documentation/Swift/CodingKeyRepresentable)
- [`Comparable`](https://developer.apple.com/documentation/Swift/Comparable)
- [`Copyable`](https://developer.apple.com/documentation/Swift/Copyable)
- [`CustomStringConvertible`](https://developer.apple.com/documentation/Swift/CustomStringConvertible)
- [`Decodable`](https://developer.apple.com/documentation/Swift/Decodable)
- [`Encodable`](https://developer.apple.com/documentation/Swift/Encodable)
- [`Equatable`](https://developer.apple.com/documentation/Swift/Equatable)
- [`Hashable`](https://developer.apple.com/documentation/Swift/Hashable)
- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)

## [See Also](https://developer.apple.com/documentation/testing/tag\#see-also)

### [Supporting types](https://developer.apple.com/documentation/testing/tag\#Supporting-types)

[`struct Bug`](https://developer.apple.com/documentation/testing/bug)

A type that represents a bug report tracked by a test.

[`struct Comment`](https://developer.apple.com/documentation/testing/comment)

A type that represents a comment related to a test.

[`struct ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait)

A type that defines a condition which must be satisfied for the testing library to enable a test.

[`struct ParallelizationTrait`](https://developer.apple.com/documentation/testing/parallelizationtrait)

A type that defines whether the testing library runs this test serially or in parallel.

[`struct List`](https://developer.apple.com/documentation/testing/tag/list)

A type representing one or more tags applied to a test.

[`struct TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait)

A type that defines a time limit to apply to a test.

Current page is Tag

## SuiteTrait Protocol
[Skip Navigation](https://developer.apple.com/documentation/testing/suitetrait#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- SuiteTrait

Protocol

# SuiteTrait

A protocol describing a trait that you can add to a test suite.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
protocol SuiteTrait : Trait
```

## [Overview](https://developer.apple.com/documentation/testing/suitetrait\#overview)

The testing library defines a number of traits that you can add to test suites. You can also define your own traits by creating types that conform to this protocol, or to the [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait) protocol.

## [Topics](https://developer.apple.com/documentation/testing/suitetrait\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/suitetrait\#Instance-Properties)

[`var isRecursive: Bool`](https://developer.apple.com/documentation/testing/suitetrait/isrecursive)

Whether this instance should be applied recursively to child test suites and test functions.

**Required** Default implementation provided.

## [Relationships](https://developer.apple.com/documentation/testing/suitetrait\#relationships)

### [Inherits From](https://developer.apple.com/documentation/testing/suitetrait\#inherits-from)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)
- [`Trait`](https://developer.apple.com/documentation/testing/trait)

### [Conforming Types](https://developer.apple.com/documentation/testing/suitetrait\#conforming-types)

- [`Bug`](https://developer.apple.com/documentation/testing/bug)
- [`Comment`](https://developer.apple.com/documentation/testing/comment)
- [`ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait)
- [`ParallelizationTrait`](https://developer.apple.com/documentation/testing/parallelizationtrait)
- [`Tag.List`](https://developer.apple.com/documentation/testing/tag/list)
- [`TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait)

## [See Also](https://developer.apple.com/documentation/testing/suitetrait\#see-also)

### [Creating custom traits](https://developer.apple.com/documentation/testing/suitetrait\#Creating-custom-traits)

[`protocol Trait`](https://developer.apple.com/documentation/testing/trait)

A protocol describing traits that can be added to a test function or to a test suite.

[`protocol TestTrait`](https://developer.apple.com/documentation/testing/testtrait)

A protocol describing a trait that you can add to a test function.

[`protocol TestScoping`](https://developer.apple.com/documentation/testing/testscoping)

A protocol that tells the test runner to run custom code before or after it runs a test suite or test function.

Current page is SuiteTrait

## Trait Protocol
[Skip Navigation](https://developer.apple.com/documentation/testing/trait#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Trait

Protocol

# Trait

A protocol describing traits that can be added to a test function or to a test suite.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
protocol Trait : Sendable
```

## [Overview](https://developer.apple.com/documentation/testing/trait\#overview)

The testing library defines a number of traits that can be added to test functions and to test suites. Define your own traits by creating types that conform to [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait) or [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait):

[`TestTrait`](https://developer.apple.com/documentation/testing/testtrait)

Conform to this type in traits that you add to test functions.

[`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait)

Conform to this type in traits that you add to test suites.

You can add a trait that conforms to both [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait) and [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait) to test functions and test suites.

## [Topics](https://developer.apple.com/documentation/testing/trait\#topics)

### [Enabling and disabling tests](https://developer.apple.com/documentation/testing/trait\#Enabling-and-disabling-tests)

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

### [Controlling how tests are run](https://developer.apple.com/documentation/testing/trait\#Controlling-how-tests-are-run)

[`static func timeLimit(TimeLimitTrait.Duration) -> Self`](https://developer.apple.com/documentation/testing/trait/timelimit(_:))

Construct a time limit trait that causes a test to time out if it runs for too long.

[`static var serialized: ParallelizationTrait`](https://developer.apple.com/documentation/testing/trait/serialized)

A trait that serializes the test to which it is applied.

### [Categorizing tests and adding information](https://developer.apple.com/documentation/testing/trait\#Categorizing-tests-and-adding-information)

[`static func tags(Tag...) -> Self`](https://developer.apple.com/documentation/testing/trait/tags(_:))

Construct a list of tags to apply to a test.

[`var comments: [Comment]`](https://developer.apple.com/documentation/testing/trait/comments)

The user-provided comments for this trait.

**Required** Default implementation provided.

### [Associating bugs](https://developer.apple.com/documentation/testing/trait\#Associating-bugs)

[`static func bug(String, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:_:))

Constructs a bug to track with a test.

[`static func bug(String?, id: String, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-10yf5)

Constructs a bug to track with a test.

[`static func bug(String?, id: some Numeric, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-3vtpl)

Constructs a bug to track with a test.

### [Running code before and after a test or suite](https://developer.apple.com/documentation/testing/trait\#Running-code-before-and-after-a-test-or-suite)

[`protocol TestScoping`](https://developer.apple.com/documentation/testing/testscoping)

A protocol that tells the test runner to run custom code before or after it runs a test suite or test function.

[`func scopeProvider(for: Test, testCase: Test.Case?) -> Self.TestScopeProvider?`](https://developer.apple.com/documentation/testing/trait/scopeprovider(for:testcase:))

Get this trait’s scope provider for the specified test and optional test case.

**Required** Default implementations provided.

[`associatedtype TestScopeProvider : TestScoping = Never`](https://developer.apple.com/documentation/testing/trait/testscopeprovider)

The type of the test scope provider for this trait.

**Required**

[`func prepare(for: Test) async throws`](https://developer.apple.com/documentation/testing/trait/prepare(for:))

Prepare to run the test that has this trait.

**Required** Default implementation provided.

## [Relationships](https://developer.apple.com/documentation/testing/trait\#relationships)

### [Inherits From](https://developer.apple.com/documentation/testing/trait\#inherits-from)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)

### [Inherited By](https://developer.apple.com/documentation/testing/trait\#inherited-by)

- [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait)
- [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait)

### [Conforming Types](https://developer.apple.com/documentation/testing/trait\#conforming-types)

- [`Bug`](https://developer.apple.com/documentation/testing/bug)
- [`Comment`](https://developer.apple.com/documentation/testing/comment)
- [`ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait)
- [`ParallelizationTrait`](https://developer.apple.com/documentation/testing/parallelizationtrait)
- [`Tag.List`](https://developer.apple.com/documentation/testing/tag/list)
- [`TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait)

## [See Also](https://developer.apple.com/documentation/testing/trait\#see-also)

### [Creating custom traits](https://developer.apple.com/documentation/testing/trait\#Creating-custom-traits)

[`protocol TestTrait`](https://developer.apple.com/documentation/testing/testtrait)

A protocol describing a trait that you can add to a test function.

[`protocol SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait)

A protocol describing a trait that you can add to a test suite.

[`protocol TestScoping`](https://developer.apple.com/documentation/testing/testscoping)

A protocol that tells the test runner to run custom code before or after it runs a test suite or test function.

Current page is Trait

## Expectation Failed Error
[Skip Navigation](https://developer.apple.com/documentation/testing/expectationfailederror#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- ExpectationFailedError

Structure

# ExpectationFailedError

A type describing an error thrown when an expectation fails during evaluation.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct ExpectationFailedError
```

## [Overview](https://developer.apple.com/documentation/testing/expectationfailederror\#overview)

The testing library throws instances of this type when the `#require()` macro records an issue.

## [Topics](https://developer.apple.com/documentation/testing/expectationfailederror\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/expectationfailederror\#Instance-Properties)

[`var expectation: Expectation`](https://developer.apple.com/documentation/testing/expectationfailederror/expectation)

The expectation that failed.

## [Relationships](https://developer.apple.com/documentation/testing/expectationfailederror\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/expectationfailederror\#conforms-to)

- [`Error`](https://developer.apple.com/documentation/Swift/Error)
- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)

## [See Also](https://developer.apple.com/documentation/testing/expectationfailederror\#see-also)

### [Retrieving information about checked expectations](https://developer.apple.com/documentation/testing/expectationfailederror\#Retrieving-information-about-checked-expectations)

[`struct Expectation`](https://developer.apple.com/documentation/testing/expectation)

A type describing an expectation that has been evaluated.

[`protocol CustomTestStringConvertible`](https://developer.apple.com/documentation/testing/customteststringconvertible)

A protocol describing types with a custom string representation when presented as part of a test’s output.

Current page is ExpectationFailedError

## Time Limit Trait
[Skip Navigation](https://developer.apple.com/documentation/testing/timelimittrait#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- TimeLimitTrait

Structure

# TimeLimitTrait

A type that defines a time limit to apply to a test.

iOS 16.0+iPadOS 16.0+Mac Catalyst 16.0+macOS 13.0+tvOS 16.0+visionOSwatchOS 9.0+Swift 6.0+Xcode 16.0+

```
struct TimeLimitTrait
```

## [Overview](https://developer.apple.com/documentation/testing/timelimittrait\#overview)

To add this trait to a test, use [`timeLimit(_:)`](https://developer.apple.com/documentation/testing/trait/timelimit(_:)).

## [Topics](https://developer.apple.com/documentation/testing/timelimittrait\#topics)

### [Structures](https://developer.apple.com/documentation/testing/timelimittrait\#Structures)

[`struct Duration`](https://developer.apple.com/documentation/testing/timelimittrait/duration)

A type representing the duration of a time limit applied to a test.

### [Instance Properties](https://developer.apple.com/documentation/testing/timelimittrait\#Instance-Properties)

[`var isRecursive: Bool`](https://developer.apple.com/documentation/testing/timelimittrait/isrecursive)

Whether this instance should be applied recursively to child test suites and test functions.

[`var timeLimit: Duration`](https://developer.apple.com/documentation/testing/timelimittrait/timelimit)

The maximum amount of time a test may run for before timing out.

### [Type Aliases](https://developer.apple.com/documentation/testing/timelimittrait\#Type-Aliases)

[`typealias TestScopeProvider`](https://developer.apple.com/documentation/testing/timelimittrait/testscopeprovider)

The type of the test scope provider for this trait.

### [Default Implementations](https://developer.apple.com/documentation/testing/timelimittrait\#Default-Implementations)

[API Reference\\
Trait Implementations](https://developer.apple.com/documentation/testing/timelimittrait/trait-implementations)

## [Relationships](https://developer.apple.com/documentation/testing/timelimittrait\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/timelimittrait\#conforms-to)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)
- [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait)
- [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait)
- [`Trait`](https://developer.apple.com/documentation/testing/trait)

## [See Also](https://developer.apple.com/documentation/testing/timelimittrait\#see-also)

### [Supporting types](https://developer.apple.com/documentation/testing/timelimittrait\#Supporting-types)

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

[`struct List`](https://developer.apple.com/documentation/testing/tag/list)

A type representing one or more tags applied to a test.

Current page is TimeLimitTrait

## Swift Expectation Type
[Skip Navigation](https://developer.apple.com/documentation/testing/expectation#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Expectation

Structure

# Expectation

A type describing an expectation that has been evaluated.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct Expectation
```

## [Topics](https://developer.apple.com/documentation/testing/expectation\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/expectation\#Instance-Properties)

[`var isPassing: Bool`](https://developer.apple.com/documentation/testing/expectation/ispassing)

Whether the expectation passed or failed.

[`var isRequired: Bool`](https://developer.apple.com/documentation/testing/expectation/isrequired)

Whether or not the expectation was required to pass.

[`var sourceLocation: SourceLocation`](https://developer.apple.com/documentation/testing/expectation/sourcelocation)

The source location where this expectation was evaluated.

## [Relationships](https://developer.apple.com/documentation/testing/expectation\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/expectation\#conforms-to)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)

## [See Also](https://developer.apple.com/documentation/testing/expectation\#see-also)

### [Retrieving information about checked expectations](https://developer.apple.com/documentation/testing/expectation\#Retrieving-information-about-checked-expectations)

[`struct ExpectationFailedError`](https://developer.apple.com/documentation/testing/expectationfailederror)

A type describing an error thrown when an expectation fails during evaluation.

[`protocol CustomTestStringConvertible`](https://developer.apple.com/documentation/testing/customteststringconvertible)

A protocol describing types with a custom string representation when presented as part of a test’s output.

Current page is Expectation

## Parameterized Testing in Swift
[Skip Navigation](https://developer.apple.com/documentation/testing/parameterizedtesting#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Implementing parameterized tests

Article

# Implementing parameterized tests

Specify different input parameters to generate multiple test cases from a test function.

## [Overview](https://developer.apple.com/documentation/testing/parameterizedtesting\#Overview)

Some tests need to be run over many different inputs. For instance, a test might need to validate all cases of an enumeration. The testing library lets developers specify one or more collections to iterate over during testing, with the elements of those collections being forwarded to a test function. An invocation of a test function with a particular set of argument values is called a test _case_.

By default, the test cases of a test function run in parallel with each other. For more information about test parallelization, see [Running tests serially or in parallel](https://developer.apple.com/documentation/testing/parallelization).

### [Parameterize over an array of values](https://developer.apple.com/documentation/testing/parameterizedtesting\#Parameterize-over-an-array-of-values)

It is very common to want to run a test _n_ times over an array containing the values that should be tested. Consider the following test function:

```
enum Food {
  case burger, iceCream, burrito, noodleBowl, kebab
}

@Test("All foods available")
func foodsAvailable() async throws {
  for food: Food in [.burger, .iceCream, .burrito, .noodleBowl, .kebab] {
    let foodTruck = FoodTruck(selling: food)
    #expect(await foodTruck.cook(food))
  }
}

```

If this test function fails for one of the values in the array, it may be unclear which value failed. Instead, the test function can be _parameterized over_ the various inputs:

```
enum Food {
  case burger, iceCream, burrito, noodleBowl, kebab
}

@Test("All foods available", arguments: [Food.burger, .iceCream, .burrito, .noodleBowl, .kebab])
func foodAvailable(_ food: Food) async throws {
  let foodTruck = FoodTruck(selling: food)
  #expect(await foodTruck.cook(food))
}

```

When passing a collection to the `@Test` attribute for parameterization, the testing library passes each element in the collection, one at a time, to the test function as its first (and only) argument. Then, if the test fails for one or more inputs, the corresponding diagnostics can clearly indicate which inputs to examine.

### [Parameterize over the cases of an enumeration](https://developer.apple.com/documentation/testing/parameterizedtesting\#Parameterize-over-the-cases-of-an-enumeration)

The previous example includes a hard-coded list of `Food` cases to test. If `Food` is an enumeration that conforms to `CaseIterable`, you can instead write:

```
enum Food: CaseIterable {
  case burger, iceCream, burrito, noodleBowl, kebab
}

@Test("All foods available", arguments: Food.allCases)
func foodAvailable(_ food: Food) async throws {
  let foodTruck = FoodTruck(selling: food)
  #expect(await foodTruck.cook(food))
}

```

This way, if a new case is added to the `Food` enumeration, it’s automatically tested by this function.

### [Parameterize over a range of integers](https://developer.apple.com/documentation/testing/parameterizedtesting\#Parameterize-over-a-range-of-integers)

It is possible to parameterize a test function over a closed range of integers:

```
@Test("Can make large orders", arguments: 1 ... 100)
func makeLargeOrder(count: Int) async throws {
  let foodTruck = FoodTruck(selling: .burger)
  #expect(await foodTruck.cook(.burger, quantity: count))
}

```

### [Test with more than one collection](https://developer.apple.com/documentation/testing/parameterizedtesting\#Test-with-more-than-one-collection)

It’s possible to test more than one collection. Consider the following test function:

```
@Test("Can make large orders", arguments: Food.allCases, 1 ... 100)
func makeLargeOrder(of food: Food, count: Int) async throws {
  let foodTruck = FoodTruck(selling: food)
  #expect(await foodTruck.cook(food, quantity: count))
}

```

Elements from the first collection are passed as the first argument to the test function, elements from the second collection are passed as the second argument, and so forth.

Assuming there are five cases in the `Food` enumeration, this test function will, when run, be invoked 500 times (5 x 100) with every possible combination of food and order size. These combinations are referred to as the collections’ Cartesian product.

To avoid the combinatoric semantics shown above, use [`zip()`](https://developer.apple.com/documentation/swift/zip(_:_:)):

```
@Test("Can make large orders", arguments: zip(Food.allCases, 1 ... 100))
func makeLargeOrder(of food: Food, count: Int) async throws {
  let foodTruck = FoodTruck(selling: food)
  #expect(await foodTruck.cook(food, quantity: count))
}

```

The zipped sequence will be “destructured” into two arguments automatically, then passed to the test function for evaluation.

This revised test function is invoked once for each tuple in the zipped sequence, for a total of five invocations instead of 500 invocations. In other words, this test function is passed the inputs `(.burger, 1)`, `(.iceCream, 2)`, …, `(.kebab, 5)` instead of `(.burger, 1)`, `(.burger, 2)`, `(.burger, 3)`, …, `(.kebab, 99)`, `(.kebab, 100)`.

### [Run selected test cases](https://developer.apple.com/documentation/testing/parameterizedtesting\#Run-selected-test-cases)

If a parameterized test meets certain requirements, the testing library allows people to run specific test cases it contains. This can be useful when a test has many cases but only some are failing since it enables re-running and debugging the failing cases in isolation.

To support running selected test cases, it must be possible to deterministically match the test case’s arguments. When someone attempts to run selected test cases of a parameterized test function, the testing library evaluates each argument of the tests’ cases for conformance to one of several known protocols, and if all arguments of a test case conform to one of those protocols, that test case can be run selectively. The following lists the known protocols, in precedence order (highest to lowest):

1. [`CustomTestArgumentEncodable`](https://developer.apple.com/documentation/testing/customtestargumentencodable)

2. `RawRepresentable`, where `RawValue` conforms to `Encodable`

3. `Encodable`

4. `Identifiable`, where `ID` conforms to `Encodable`


If any argument of a test case doesn’t meet one of the above requirements, then the overall test case cannot be run selectively.

## [See Also](https://developer.apple.com/documentation/testing/parameterizedtesting\#see-also)

### [Test parameterization](https://developer.apple.com/documentation/testing/parameterizedtesting\#Test-parameterization)

[`macro Test<C>(String?, any TestTrait..., arguments: C)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-8kn7a)

Declare a test parameterized over a collection of values.

[`macro Test<C1, C2>(String?, any TestTrait..., arguments: C1, C2)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:_:))

Declare a test parameterized over two collections of values.

[`macro Test<C1, C2>(String?, any TestTrait..., arguments: Zip2Sequence<C1, C2>)`](https://developer.apple.com/documentation/testing/test(_:_:arguments:)-3rzok)

Declare a test parameterized over two zipped collections of values.

[`protocol CustomTestArgumentEncodable`](https://developer.apple.com/documentation/testing/customtestargumentencodable)

A protocol for customizing how arguments passed to parameterized tests are encoded, which is used to match against when running specific arguments.

[`struct Case`](https://developer.apple.com/documentation/testing/test/case)

A single test case from a parameterized [`Test`](https://developer.apple.com/documentation/testing/test).

Current page is Implementing parameterized tests

## Condition Trait
[Skip Navigation](https://developer.apple.com/documentation/testing/conditiontrait#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- ConditionTrait

Structure

# ConditionTrait

A type that defines a condition which must be satisfied for the testing library to enable a test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct ConditionTrait
```

## [Mentioned in](https://developer.apple.com/documentation/testing/conditiontrait\#mentions)

[Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)

## [Overview](https://developer.apple.com/documentation/testing/conditiontrait\#overview)

To add this trait to a test, use one of the following functions:

- [`enabled(if:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/trait/enabled(if:_:sourcelocation:))

- [`enabled(_:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/trait/enabled(_:sourcelocation:_:))

- [`disabled(_:sourceLocation:)`](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:))

- [`disabled(if:_:sourceLocation:)`](https://developer.apple.com/documentation/testing/trait/disabled(if:_:sourcelocation:))

- [`disabled(_:sourceLocation:_:)`](https://developer.apple.com/documentation/testing/trait/disabled(_:sourcelocation:_:))


## [Topics](https://developer.apple.com/documentation/testing/conditiontrait\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/conditiontrait\#Instance-Properties)

[`var comments: [Comment]`](https://developer.apple.com/documentation/testing/conditiontrait/comments)

The user-provided comments for this trait.

[`var isRecursive: Bool`](https://developer.apple.com/documentation/testing/conditiontrait/isrecursive)

Whether this instance should be applied recursively to child test suites and test functions.

[`var sourceLocation: SourceLocation`](https://developer.apple.com/documentation/testing/conditiontrait/sourcelocation)

The source location where this trait is specified.

### [Instance Methods](https://developer.apple.com/documentation/testing/conditiontrait\#Instance-Methods)

[`func prepare(for: Test) async throws`](https://developer.apple.com/documentation/testing/conditiontrait/prepare(for:))

Prepare to run the test that has this trait.

### [Type Aliases](https://developer.apple.com/documentation/testing/conditiontrait\#Type-Aliases)

[`typealias TestScopeProvider`](https://developer.apple.com/documentation/testing/conditiontrait/testscopeprovider)

The type of the test scope provider for this trait.

### [Default Implementations](https://developer.apple.com/documentation/testing/conditiontrait\#Default-Implementations)

[API Reference\\
Trait Implementations](https://developer.apple.com/documentation/testing/conditiontrait/trait-implementations)

## [Relationships](https://developer.apple.com/documentation/testing/conditiontrait\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/conditiontrait\#conforms-to)

- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)
- [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait)
- [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait)
- [`Trait`](https://developer.apple.com/documentation/testing/trait)

## [See Also](https://developer.apple.com/documentation/testing/conditiontrait\#see-also)

### [Supporting types](https://developer.apple.com/documentation/testing/conditiontrait\#Supporting-types)

[`struct Bug`](https://developer.apple.com/documentation/testing/bug)

A type that represents a bug report tracked by a test.

[`struct Comment`](https://developer.apple.com/documentation/testing/comment)

A type that represents a comment related to a test.

[`struct ParallelizationTrait`](https://developer.apple.com/documentation/testing/parallelizationtrait)

A type that defines whether the testing library runs this test serially or in parallel.

[`struct Tag`](https://developer.apple.com/documentation/testing/tag)

A type representing a tag that can be applied to a test.

[`struct List`](https://developer.apple.com/documentation/testing/tag/list)

A type representing one or more tags applied to a test.

[`struct TimeLimitTrait`](https://developer.apple.com/documentation/testing/timelimittrait)

A type that defines a time limit to apply to a test.

Current page is ConditionTrait

## SourceLocation in Swift
[Skip Navigation](https://developer.apple.com/documentation/testing/sourcelocation#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- SourceLocation

Structure

# SourceLocation

A type representing a location in source code.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct SourceLocation
```

## [Topics](https://developer.apple.com/documentation/testing/sourcelocation\#topics)

### [Initializers](https://developer.apple.com/documentation/testing/sourcelocation\#Initializers)

[`init(fileID: String, filePath: String, line: Int, column: Int)`](https://developer.apple.com/documentation/testing/sourcelocation/init(fileid:filepath:line:column:))

Initialize an instance of this type with the specified location details.

### [Instance Properties](https://developer.apple.com/documentation/testing/sourcelocation\#Instance-Properties)

[`var column: Int`](https://developer.apple.com/documentation/testing/sourcelocation/column)

The column in the source file.

[`var fileID: String`](https://developer.apple.com/documentation/testing/sourcelocation/fileid)

The file ID of the source file.

[`var fileName: String`](https://developer.apple.com/documentation/testing/sourcelocation/filename)

The name of the source file.

[`var line: Int`](https://developer.apple.com/documentation/testing/sourcelocation/line)

The line in the source file.

[`var moduleName: String`](https://developer.apple.com/documentation/testing/sourcelocation/modulename)

The name of the module containing the source file.

### [Default Implementations](https://developer.apple.com/documentation/testing/sourcelocation\#Default-Implementations)

[API Reference\\
Comparable Implementations](https://developer.apple.com/documentation/testing/sourcelocation/comparable-implementations)

[API Reference\\
CustomDebugStringConvertible Implementations](https://developer.apple.com/documentation/testing/sourcelocation/customdebugstringconvertible-implementations)

[API Reference\\
CustomStringConvertible Implementations](https://developer.apple.com/documentation/testing/sourcelocation/customstringconvertible-implementations)

[API Reference\\
Decodable Implementations](https://developer.apple.com/documentation/testing/sourcelocation/decodable-implementations)

[API Reference\\
Encodable Implementations](https://developer.apple.com/documentation/testing/sourcelocation/encodable-implementations)

[API Reference\\
Equatable Implementations](https://developer.apple.com/documentation/testing/sourcelocation/equatable-implementations)

[API Reference\\
Hashable Implementations](https://developer.apple.com/documentation/testing/sourcelocation/hashable-implementations)

## [Relationships](https://developer.apple.com/documentation/testing/sourcelocation\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/sourcelocation\#conforms-to)

- [`Comparable`](https://developer.apple.com/documentation/Swift/Comparable)
- [`Copyable`](https://developer.apple.com/documentation/Swift/Copyable)
- [`CustomDebugStringConvertible`](https://developer.apple.com/documentation/Swift/CustomDebugStringConvertible)
- [`CustomStringConvertible`](https://developer.apple.com/documentation/Swift/CustomStringConvertible)
- [`Decodable`](https://developer.apple.com/documentation/Swift/Decodable)
- [`Encodable`](https://developer.apple.com/documentation/Swift/Encodable)
- [`Equatable`](https://developer.apple.com/documentation/Swift/Equatable)
- [`Hashable`](https://developer.apple.com/documentation/Swift/Hashable)
- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)

Current page is SourceLocation

## Bug Reporting Structure
[Skip Navigation](https://developer.apple.com/documentation/testing/bug#app-main)

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Bug

Structure

# Bug

A type that represents a bug report tracked by a test.

iOSiPadOSMac CatalystmacOStvOSvisionOSwatchOSSwift 6.0+Xcode 16.0+

```
struct Bug
```

## [Mentioned in](https://developer.apple.com/documentation/testing/bug\#mentions)

[Interpreting bug identifiers](https://developer.apple.com/documentation/testing/bugidentifiers)

[Adding comments to tests](https://developer.apple.com/documentation/testing/addingcomments)

## [Overview](https://developer.apple.com/documentation/testing/bug\#overview)

To add this trait to a test, use one of the following functions:

- [`bug(_:_:)`](https://developer.apple.com/documentation/testing/trait/bug(_:_:))

- [`bug(_:id:_:)`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-10yf5)

- [`bug(_:id:_:)`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-3vtpl)


## [Topics](https://developer.apple.com/documentation/testing/bug\#topics)

### [Instance Properties](https://developer.apple.com/documentation/testing/bug\#Instance-Properties)

[`var id: String?`](https://developer.apple.com/documentation/testing/bug/id)

A unique identifier in this bug’s associated bug-tracking system, if available.

[`var title: Comment?`](https://developer.apple.com/documentation/testing/bug/title)

The human-readable title of the bug, if specified by the test author.

[`var url: String?`](https://developer.apple.com/documentation/testing/bug/url)

A URL that links to more information about the bug, if available.

### [Default Implementations](https://developer.apple.com/documentation/testing/bug\#Default-Implementations)

[API Reference\\
Decodable Implementations](https://developer.apple.com/documentation/testing/bug/decodable-implementations)

[API Reference\\
Encodable Implementations](https://developer.apple.com/documentation/testing/bug/encodable-implementations)

[API Reference\\
Equatable Implementations](https://developer.apple.com/documentation/testing/bug/equatable-implementations)

[API Reference\\
Hashable Implementations](https://developer.apple.com/documentation/testing/bug/hashable-implementations)

[API Reference\\
SuiteTrait Implementations](https://developer.apple.com/documentation/testing/bug/suitetrait-implementations)

[API Reference\\
Trait Implementations](https://developer.apple.com/documentation/testing/bug/trait-implementations)

## [Relationships](https://developer.apple.com/documentation/testing/bug\#relationships)

### [Conforms To](https://developer.apple.com/documentation/testing/bug\#conforms-to)

- [`Copyable`](https://developer.apple.com/documentation/Swift/Copyable)
- [`Decodable`](https://developer.apple.com/documentation/Swift/Decodable)
- [`Encodable`](https://developer.apple.com/documentation/Swift/Encodable)
- [`Equatable`](https://developer.apple.com/documentation/Swift/Equatable)
- [`Hashable`](https://developer.apple.com/documentation/Swift/Hashable)
- [`Sendable`](https://developer.apple.com/documentation/Swift/Sendable)
- [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait)
- [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait)
- [`Trait`](https://developer.apple.com/documentation/testing/trait)

## [See Also](https://developer.apple.com/documentation/testing/bug\#see-also)

### [Supporting types](https://developer.apple.com/documentation/testing/bug\#Supporting-types)

[`struct Comment`](https://developer.apple.com/documentation/testing/comment)

A type that represents a comment related to a test.

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

Current page is Bug

## Swift Test Traits
[Skip Navigation](https://developer.apple.com/documentation/testing/traits#app-main)

Collection

- [Swift Testing](https://developer.apple.com/documentation/testing)
- Traits

API Collection

# Traits

Annotate test functions and suites, and customize their behavior.

## [Overview](https://developer.apple.com/documentation/testing/traits\#Overview)

Pass built-in traits to test functions or suite types to comment, categorize, classify, and modify the runtime behavior of test suites and test functions. Implement the [`TestTrait`](https://developer.apple.com/documentation/testing/testtrait), and [`SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait) protocols to create your own types that customize the behavior of your tests.

## [Topics](https://developer.apple.com/documentation/testing/traits\#topics)

### [Customizing runtime behaviors](https://developer.apple.com/documentation/testing/traits\#Customizing-runtime-behaviors)

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

[`static func timeLimit(TimeLimitTrait.Duration) -> Self`](https://developer.apple.com/documentation/testing/trait/timelimit(_:))

Construct a time limit trait that causes a test to time out if it runs for too long.

### [Running tests serially or in parallel](https://developer.apple.com/documentation/testing/traits\#Running-tests-serially-or-in-parallel)

[Running tests serially or in parallel](https://developer.apple.com/documentation/testing/parallelization)

Control whether tests run serially or in parallel.

[`static var serialized: ParallelizationTrait`](https://developer.apple.com/documentation/testing/trait/serialized)

A trait that serializes the test to which it is applied.

### [Annotating tests](https://developer.apple.com/documentation/testing/traits\#Annotating-tests)

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

[`static func bug(String, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:_:))

Constructs a bug to track with a test.

[`static func bug(String?, id: String, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-10yf5)

Constructs a bug to track with a test.

[`static func bug(String?, id: some Numeric, Comment?) -> Self`](https://developer.apple.com/documentation/testing/trait/bug(_:id:_:)-3vtpl)

Constructs a bug to track with a test.

### [Creating custom traits](https://developer.apple.com/documentation/testing/traits\#Creating-custom-traits)

[`protocol Trait`](https://developer.apple.com/documentation/testing/trait)

A protocol describing traits that can be added to a test function or to a test suite.

[`protocol TestTrait`](https://developer.apple.com/documentation/testing/testtrait)

A protocol describing a trait that you can add to a test function.

[`protocol SuiteTrait`](https://developer.apple.com/documentation/testing/suitetrait)

A protocol describing a trait that you can add to a test suite.

[`protocol TestScoping`](https://developer.apple.com/documentation/testing/testscoping)

A protocol that tells the test runner to run custom code before or after it runs a test suite or test function.

### [Supporting types](https://developer.apple.com/documentation/testing/traits\#Supporting-types)

[`struct Bug`](https://developer.apple.com/documentation/testing/bug)

A type that represents a bug report tracked by a test.

[`struct Comment`](https://developer.apple.com/documentation/testing/comment)

A type that represents a comment related to a test.

[`struct ConditionTrait`](https://developer.apple.com/documentation/testing/conditiontrait)

A type that defines a condition which must be satisfied for the testing library to enable a test.

