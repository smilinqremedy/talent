#!/usr/bin/env python3
"""
Python Types, Dynamic Typing, and Developer Velocity
Hands-on demonstrations showing Python's type system, dynamic reassignment,
strong typing enforcement, runtime type errors, and optional type annotations.
"""


def banner(title: str) -> None:
    print(f"\n{'=' * 65}")
    print(f" {title}")
    print(f"{'=' * 65}\n")


def demo_dynamic_reassignment() -> None:
    banner("Demo 1: Variables Have No Fixed Type; Objects Do")
    print("In Python, a variable is just a name tag pointing to an object.")
    print("Watch the variable 'x' point to completely different types over time:\n")

    x = 42
    print(f"Value: {str(x):<12} Type: {type(x).__name__:<8} Memory ID: {id(x)}")

    x = "now"
    print(f"Value: {str(x):<12} Type: {type(x).__name__:<8} Memory ID: {id(x)}")

    x = [1, 2, 3]
    print(f"Value: {str(x):<12} Type: {type(x).__name__:<8} Memory ID: {id(x)}")

    print("\nTakeaway: The variable 'x' itself has no fixed type.")
    print("The type belongs entirely to the object currently referenced in memory.")


def demo_strong_typing() -> None:
    banner("Demo 2: Dynamic Typing vs. Strong Typing")
    print("Python is dynamic, but it is also STRONGLY typed.")
    print("It will NOT silently coerce incompatible types like weak languages do:\n")

    print("Attempting: '1' + 2")
    try:
        _ = "1" + 2
    except TypeError as e:
        print(f"  -> Caught TypeError: {e}")

    print("\nAttempting: 'I am ' + 25")
    try:
        age = 25
        _ = "I am " + age
    except TypeError as e:
        print(f"  -> Caught TypeError: {e}")

    print("\nCorrect explicit conversion:")
    valid_message = "I am " + str(25)
    print(f"  -> Result: '{valid_message}'")

    print("\nTakeaway: Python refuses implicit dangerous type conversions.")
    print("You must convert types explicitly, preventing silent corruption.")


def demo_runtime_error_tradeoff() -> None:
    banner("Demo 3: The Runtime Trade-Off (Latent Type Errors)")
    print("Because types are checked during execution, bugs in untested branches")
    print("can hide until triggered in production:\n")

    def process_order(order_id: int, is_priority: bool = False):
        print(f"Processing Order #{order_id}...")
        if is_priority:
            # Latent bug: fee is a string, incompatible with float addition
            fee = "500"
            return fee + 150.0
        return 100.0

    print("1. Running standard order (healthy branch):")
    normal_total = process_order(101, is_priority=False)
    print(f"   Success! Order total: \u20a6{normal_total:,.2f}")

    print("\n2. Running priority order (untested / rare branch):")
    try:
        process_order(102, is_priority=True)
    except TypeError as e:
        print(f"   CRASH at runtime: {e}")

    print("\nTakeaway: In statically typed languages, the compiler catches this before running.")
    print("In Python, thorough testing is essential to verify all paths.")


def demo_type_hints_inspection() -> None:
    banner("Demo 4: Optional Type Hints Are Annotations, Not Guards")
    print("Python supports PEP 484 type hints, but CPython does not enforce them at runtime:\n")

    def add_numbers(a: int, b: int) -> int:
        return a + b

    print("Inspecting function metadata:")
    print(f"  add_numbers.__annotations__ = {add_numbers.__annotations__}")

    print("\nCalling function with integers: add_numbers(10, 20)")
    int_result = add_numbers(10, 20)
    print(f"  Result: {int_result}")

    print("\nCalling function with strings: add_numbers('Lagos ', 'Market')")
    str_result = add_numbers("Lagos ", "Market")
    print(f"  Result: '{str_result}'")

    print("\nTakeaway: Type hints serve as metadata for documentation, IDE autocomplete,")
    print("and static analyzers (mypy), while Python's runtime remains dynamic.")


def main() -> None:
    print("=== Python Types, Dynamic Typing, and Developer Velocity ===")
    demo_dynamic_reassignment()
    demo_strong_typing()
    demo_runtime_error_tradeoff()
    demo_type_hints_inspection()
    print("\nAll dynamic typing demonstrations completed successfully!")


if __name__ == "__main__":
    main()
