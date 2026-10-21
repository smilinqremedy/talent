#!/usr/bin/env python3
"""
The Python Data & AI Ecosystem: The Power of the Glue Language
Hands-on demonstrations showing:
1. Performance differences between pure Python and NumPy's compiled C backend.
2. Contiguous C memory layout vs. Python pointer overhead.
3. Vectorized calculations without explicit loops.
4. An end-to-end Lagos fintech transaction pipeline using Pandas.
"""

import time
import numpy as np
import pandas as pd


def banner(title: str) -> None:
    print(f"\n{'=' * 65}")
    print(f" {title}")
    print(f"{'=' * 65}\n")


def demo_glue_speed_benchmark() -> None:
    banner("Demo 1: The Glue Language Speed Reality")
    print("Python itself is not fast at heavy number-crunching.")
    print("Its power comes from gluing easy syntax to compiled C/Fortran/CUDA libraries.")
    print("Benchmarking 1,500,000 price calculations (multiplying by 0.9):\n")

    n = 1_500_000
    py_list = list(range(n))
    np_arr = np.arange(n)

    # 1. Pure Python loop
    t0 = time.perf_counter()
    _ = [x * 0.9 for x in py_list]
    t_py = time.perf_counter() - t0

    # 2. NumPy C-backend
    t0 = time.perf_counter()
    _ = np_arr * 0.9
    t_np = time.perf_counter() - t0

    speedup = t_py / t_np if t_np > 0 else 1.0
    print(f"Pure Python Loop (CPython bytecode) : {t_py:.4f} seconds")
    print(f"NumPy C-Backend (compiled C loops)   : {t_np:.4f} seconds")
    print(f"Speedup Factor                       : {speedup:.1f}x faster!")

    print("\nTakeaway: You write readable Python, but optimized C runs the heavy math.")


def demo_memory_contiguity() -> None:
    banner("Demo 2: Contiguous C Memory vs. Python Pointer Lists")
    print("Why is the C backend so much faster? Memory layout.\n")

    np_arr = np.array([1200, 3500, 800, 2500], dtype=np.int64)

    print("NumPy Array Object:")
    print(f"  Data Type (dtype)       : {np_arr.dtype}")
    print(f"  Bytes per item          : {np_arr.itemsize} bytes")
    print(f"  Total array buffer size : {np_arr.nbytes} bytes")
    print(f"  Byte stride to next item: {np_arr.strides[0]} bytes (adjacent in physical RAM)")

    print("\nTakeaway: In a Python list, each number is a separate PyObject in memory")
    print("connected by pointers. NumPy stores raw numbers in a contiguous memory block,")
    print("enabling modern CPU SIMD vector registers and hardware cache efficiency.")


def demo_vectorization() -> None:
    banner("Demo 3: Vectorization & Math Without Explicit Loops")
    print("Using vectorized operations on market prices:\n")

    prices = np.array([1200, 3500, 800, 2500])
    print(f"Original prices  : {prices}")

    # Broadcast operation handled entirely in compiled C
    discounted = prices * 0.9
    print(f"Discounted (90%) : {discounted}")

    # Boolean indexing without writing a single 'if' or 'for' loop
    expensive = prices[prices >= 2000]
    print(f"Prices >= \u20a62,000 : {expensive}")

    print("\nTakeaway: Vectorization replaces slow interpreter loop cycles with")
    print("single-instruction execution inside compiled C routines.")


def demo_fintech_pipeline() -> None:
    banner("Demo 4: The Lagos Fintech Data Pipeline (Pandas)")
    print("Simulating a transaction processing pipeline for a Lagos fintech startup:\n")

    raw_transactions = {
        "tx_id": [1001, 1002, 1003, 1004, 1005, 1006],
        "merchant": [
            "Ebeano Supermarket",
            "Ojuelegba Fuel Depot",
            "Ikeja Tech Store",
            "Yaba Hub Cafe",
            "Lekki Lounge",
            "Broad St Electronics",
        ],
        "city": ["Lekki", "Surulere", "Ikeja", "Yaba", "Lekki", "CMS"],
        "amount_ngn": [15500, 4200, 185000, 8500, 64000, 240000],
        "status": ["SUCCESS", "SUCCESS", "FLAGGED", "SUCCESS", "SUCCESS", "FLAGGED"],
    }

    df = pd.DataFrame(raw_transactions)
    print("1. Ingested Transaction Table:")
    print(df.to_string(index=False))

    print("\n2. High-Risk / Flagged Transactions:")
    flagged = df[df["status"] == "FLAGGED"]
    print(flagged[["tx_id", "merchant", "amount_ngn"]].to_string(index=False))

    print("\n3. Summary Aggregations:")
    total_volume = df["amount_ngn"].sum()
    successful_volume = df[df["status"] == "SUCCESS"]["amount_ngn"].sum()
    print(f"   Total Volume Processed  : \u20a6{total_volume:,}")
    print(f"   Cleared Volume (Settled): \u20a6{successful_volume:,}")

    print("\nTakeaway: From data ingestion to fraud detection and reporting,")
    print("the entire pipeline runs in high-level Python powered by fast C libraries.")


def main() -> None:
    print("=== The Python Data & AI Ecosystem: The Power of the Glue Language ===")
    demo_glue_speed_benchmark()
    demo_memory_contiguity()
    demo_vectorization()
    demo_fintech_pipeline()
    print("\nAll ecosystem demonstrations completed successfully!")


if __name__ == "__main__":
    main()
