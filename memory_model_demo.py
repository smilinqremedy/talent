#!/usr/bin/env python3
"""
The Mental Model: Talking to a Machine
Hands-on Python memory management and abstraction demonstrations.
"""

import gc
import sys


def banner(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}\n")


def demo_dynamic_memory_allocation() -> None:
    banner("Demo 1: Abstraction & Dynamic Memory Allocation")
    print("In Python, you do not declare byte sizes or reallocate buffers.")
    print("Watch Python automatically resize the list as elements are added:\n")

    fruits = []
    print(f"Initial empty list size : {sys.getsizeof(fruits)} bytes")

    items = ["mango", "pawpaw", "orange", "banana", "guava", "pineapple"]
    for fruit in items:
        fruits.append(fruit)
        print(f"Added {fruit:<10} -> Current list size in memory: {sys.getsizeof(fruits)} bytes")

    print("\nTakeaway: Python over-allocates internal buffer space so appends are fast,")
    print("handling all low-level memory reallocations behind the scenes.")


def demo_variables_as_labels() -> None:
    banner("Demo 2: Variables Are Signboards, Not Memory Slots")
    print("Variables in Python are names bound to objects in memory, not memory boxes.\n")

    stall_1 = ["Benue yam", "Abuja yam"]
    stall_2 = stall_1

    print(f"stall_1 memory ID: {id(stall_1)}")
    print(f"stall_2 memory ID: {id(stall_2)}")
    print(f"Do stall_1 and stall_2 refer to the identical object? {stall_1 is stall_2}")

    stall_2.append("Ogoja yam")
    print(f"\nAfter appending to stall_2, stall_1 is now: {stall_1}")
    print("Takeaway: Both variable names reference the same object in memory.")


def demo_reference_counting() -> None:
    banner("Demo 3: Reference Counting & Immediate Cleanup")
    print("Python uses reference counts. When the count drops to 0, memory is freed immediately.\n")

    class MarketStall:
        def __init__(self, name: str):
            self.name = name
            print(f"[OPEN] Stall '{self.name}' rented.")

        def __del__(self):
            print(f"[CLOSED] Rent expired. Stall '{self.name}' vacated and memory freed!")

    stall = MarketStall("Ojota Depot")
    print(f"Current reference count: {sys.getrefcount(stall) - 1}")

    alias = stall
    print(f"Reference count after alias: {sys.getrefcount(stall) - 1}")

    print("\nDeleting alias...")
    del alias
    print(f"Reference count after deleting alias: {sys.getrefcount(stall) - 1}")

    print("\nDeleting primary reference 'stall'...")
    del stall
    print("Notice the [CLOSED] message above executed immediately before this line!")


def demo_cyclic_garbage_collection() -> None:
    banner("Demo 4: Cyclic References & The Cycle-Detecting GC")
    print("When objects reference each other, reference counting alone cannot free them.")
    print("Python's cycle-detecting garbage collector ('the house help') steps in.\n")

    class Trader:
        def __init__(self, name: str):
            self.name = name
            self.partner = None
            print(f"Trader {self.name} entered the market.")

        def __del__(self):
            print(f"Trader {self.name} vacated from memory.")

    gc.disable()

    t1 = Trader("Amina")
    t2 = Trader("Chidi")
    t1.partner = t2
    t2.partner = t1

    print("\nDeleting global variables t1 and t2...")
    del t1
    del t2
    print("Global variables are gone, but Amina & Chidi still hold references to each other.")
    print("Notice neither trader has been freed yet.")

    print("\nManually triggering garbage collection sweep: gc.collect()...")
    collected = gc.collect()
    print(f"Sweep finished. Unreachable objects recovered: {collected}")

    gc.enable()


def main() -> None:
    print("=== Python Memory Management & Abstraction Demonstrations ===")
    demo_dynamic_memory_allocation()
    demo_variables_as_labels()
    demo_reference_counting()
    demo_cyclic_garbage_collection()
    print("\nAll demonstrations completed successfully!")


if __name__ == "__main__":
    main()
