#!/usr/bin/env python3
"""
Execution Speed vs. Implementation Speed: The Engineering Trade-Off
Hands-on demonstrations showing:
1. Why pure Python loops are slower (object boxing and interpreter overhead).
2. The escape hatch: Calling high-performance native C code via ctypes.
3. The I/O bottleneck reality: Why Python CPU time is often negligible in real-world APIs.
4. The business value of developer velocity.
"""

import ctypes
import os
import sys
import tempfile
import time


def banner(title: str) -> None:
    print(f"\n{'=' * 65}")
    print(f" {title}")
    print(f"{'=' * 65}\n")


def demo_object_overhead() -> None:
    banner("Demo 1: The Object Boxing Overhead Penalty")
    print("In low-level languages (C, C++, Rust), an integer occupies 4 to 8 bytes.")
    print("In Python, every value is a heap-allocated PyObject with metadata:\n")

    val_int = 1000
    val_float = 3.14159
    val_str = "Ibadan Wedding"
    val_list = [1, 2, 3, 4]

    print(f"Integer 1000          : {sys.getsizeof(val_int)} bytes (vs. 4-8 bytes in C)")
    print(f"Float 3.14159         : {sys.getsizeof(val_float)} bytes (vs. 8 bytes in C)")
    print(f"String 'Ibadan...'    : {sys.getsizeof(val_str)} bytes")
    print(f"List with 4 elements  : {sys.getsizeof(val_list)} bytes (plus element PyObjects)")

    print("\nTakeaway: Looping in pure Python requires unpacking and inspecting")
    print("heavyweight PyObject structures on every single iteration.")


def demo_c_bindings_escape_hatch() -> None:
    banner("Demo 2: C-Bindings — The High-Performance Escape Hatch")
    print("When computational bottlenecks occur, Python doesn't need to be replaced.")
    print("We can offload heavy loops to compiled C using ctypes:\n")

    c_source = """
    long long fast_c_sum(long long n) {
        long long total = 0;
        for (long long i = 0; i < n; i++) {
            total += i;
        }
        return total;
    }
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        c_path = os.path.join(tmpdir, "fast_sum.c")
        so_path = os.path.join(tmpdir, "fast_sum.so")

        with open(c_path, "w") as f:
            f.write(c_source)

        # Compile C source into shared library
        os.system(f"gcc -O3 -shared -fPIC -o {so_path} {c_path}")

        # Bind with Python ctypes
        lib = ctypes.CDLL(so_path)
        lib.fast_c_sum.argtypes = [ctypes.c_longlong]
        lib.fast_c_sum.restype = ctypes.c_longlong

        n = 10_000_000
        print(f"Benchmarking sum of {n:,} numbers:\n")

        # 1. Native C function called from Python
        t0 = time.perf_counter()
        c_res = lib.fast_c_sum(n)
        t_c = time.perf_counter() - t0

        # 2. Pure Python loop
        t0 = time.perf_counter()
        py_res = 0
        for i in range(n):
            py_res += i
        t_py = time.perf_counter() - t0

        speedup = t_py / t_c if t_c > 0 else 1.0
        print(f"Pure Python Loop (CPython) : {t_py:.4f} seconds (Result: {py_res:,})")
        print(f"Native C-binding (ctypes)  : {t_c:.6f} seconds (Result: {c_res:,})")
        print(f"Speedup Factor             : {speedup:.1f}x faster in compiled C!")

    print("\nTakeaway: Python acts as the coordinator while compiled C handles the compute.")


def demo_io_vs_cpu_bottleneck() -> None:
    banner("Demo 3: The I/O-Bound Bottleneck Reality")
    print("In real-world web applications and fintech APIs, response time is")
    print("dominated by database and network latency, not CPU computation:\n")

    # 1. Simulate database / network latency
    t0 = time.perf_counter()
    time.sleep(0.040)  # 40ms database query
    io_duration = time.perf_counter() - t0

    # 2. Python business logic (evaluating credit eligibility)
    t0 = time.perf_counter()
    monthly_income = 450_000
    credit_score = 720
    existing_debt = 50_000
    approved = (monthly_income > 200_000) and (credit_score > 650) and (existing_debt < 100_000)
    interest_rate = 0.12 if credit_score > 700 else 0.18
    cpu_duration = time.perf_counter() - t0

    total_time = io_duration + cpu_duration
    io_pct = (io_duration / total_time) * 100
    cpu_pct = (cpu_duration / total_time) * 100

    print(f"Database / Network I/O Time : {io_duration * 1000:.2f} ms ({io_pct:.2f}% of total request)")
    print(f"Python Business Logic Time  : {cpu_duration * 1000:.4f} ms ({cpu_pct:.2f}% of total request)")
    print(f"Total Request Latency       : {total_time * 1000:.2f} ms")
    print(f"Decision                    : Approved = {approved}, Interest Rate = {interest_rate * 100:.0f}%")

    print("\nTakeaway: Rewriting this business logic in C or Rust saves 0.005 milliseconds,")
    print("which is completely invisible to users waiting on network transmission.")


def demo_developer_velocity() -> None:
    banner("Demo 4: The Value of Developer Velocity")
    print("Implementation speed: Turning ideas into working products rapidly.")
    print("In 4 lines of Python, we ingest, filter, and summarize transactions:")

    transactions = [
        {"client": "Kemi", "amount": 25000, "status": "APPROVED"},
        {"client": "Tunde", "amount": 180000, "status": "FLAGGED"},
        {"client": "Emeka", "amount": 62000, "status": "APPROVED"},
    ]

    approved_total = sum(t["amount"] for t in transactions if t["status"] == "APPROVED")
    print(f"\nQuick Summary: Total Approved = \u20a6{approved_total:,}")

    print("\nTakeaway: In C or C++, this requires memory allocations, struct definitions,")
    print("pointers, and error checking. In Python, it takes 30 seconds to write and deploy.")


def main() -> None:
    print("=== Execution Speed vs. Implementation Speed ===")
    demo_object_overhead()
    demo_c_bindings_escape_hatch()
    demo_io_vs_cpu_bottleneck()
    demo_developer_velocity()
    print("\nAll speed trade-off demonstrations completed successfully!")


if __name__ == "__main__":
    main()
