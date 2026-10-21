#!/usr/bin/env python3
"""
CPython, Bytecode, and the Python Virtual Machine (PVM)
Hands-on demonstrations showing how Python source code compiles to bytecode
and executes on the virtual machine.
"""

import dis
import os
import py_compile
import tempfile


def banner(title: str) -> None:
    print(f"\n{'=' * 65}")
    print(f" {title}")
    print(f"{'=' * 65}\n")


def demo_bytecode_disassembly() -> None:
    banner("Demo 1: Disassembling Python into CPython Bytecode")
    print("The Python interpreter translates human-readable statements into")
    print("virtual machine opcodes. Let's disassemble our balance calculation:\n")

    def calculate_balance():
        balance = 10000
        withdrawal = 3000
        balance = balance - withdrawal
        print(balance)

    print("Source code:")
    print("  balance = 10000")
    print("  withdrawal = 3000")
    print("  balance = balance - withdrawal")
    print("  print(balance)\n")

    print("CPython Bytecode instructions (via dis.dis):")
    dis.dis(calculate_balance)

    print("\nTakeaway: The PVM reads simple stack-based opcodes like LOAD_CONST,")
    print("STORE_FAST, BINARY_OP, and CALL rather than high-level syntax.")


def demo_compile_vs_exec() -> None:
    banner("Demo 2: Proof of the Two-Stage Model (compile -> exec)")
    print("CPython compiles source code to a code object BEFORE executing it.")
    print("We can perform these two stages independently:\n")

    source_code = """
balance = 10000
withdrawal = 3000
balance = balance - withdrawal
print(f"Remaining balance: \u20a6{balance:,}")
"""

    print("--- Stage 1: compile() source code into Bytecode Object ---")
    code_obj = compile(source_code, filename="pay.py", mode="exec")
    print("Compiled Code Object :", code_obj)
    print("Constants (co_consts):", code_obj.co_consts)
    print("Variables (co_names) :", code_obj.co_names)
    print("Notice: No calculations or prints have happened yet!")

    print("\n--- Stage 2: Handing bytecode to the PVM via exec() ---")
    exec(code_obj)
    print("Takeaway: Compilation and execution are strictly separate stages in CPython.")


def demo_raw_code_object_bytes() -> None:
    banner("Demo 3: Peeking Inside Raw Bytecode Bytes")
    print("Bytecode is an internal binary representation. Let's examine the raw bytes:\n")

    def simple_sub():
        x = 10
        return x - 5

    code = simple_sub.__code__
    raw_bytes = list(code.co_code)

    print(f"Function Name     : {code.co_name}")
    print(f"Raw Opcode Bytes  : {raw_bytes}")
    print(f"Constants Table   : {code.co_consts}")
    print(f"Local Names Table : {code.co_varnames}")

    print("\nTakeaway: The PVM consumes a sequence of numerical bytes where each")
    print("number maps to a CPython virtual machine instruction.")


def demo_pyc_caching() -> None:
    banner("Demo 4: Bytecode Caching and .pyc Files")
    print("CPython stores compiled bytecode in .pyc files to speed up startup on re-runs:\n")

    with tempfile.TemporaryDirectory() as tmpdir:
        src_file = os.path.join(tmpdir, "pay.py")
        with open(src_file, "w") as f:
            f.write("def process():\n    return 'Payment successful!'\n")

        # Compile to .pyc
        pyc_file = py_compile.compile(src_file)

        src_size = os.path.getsize(src_file)
        pyc_size = os.path.getsize(pyc_file) if pyc_file else 0

        print(f"Source file (.py)       : {src_file}")
        print(f"Source file size        : {src_size} bytes")
        print(f"Compiled bytecode (.pyc): {pyc_file}")
        print(f"Bytecode file size      : {pyc_size} bytes")

    print("\nTakeaway: .pyc files contain cached bytecode headers and code objects.")
    print("They are platform-independent bytecode caches, NOT standalone OS executables.")


def main() -> None:
    print("=== CPython, Bytecode, and the Python Virtual Machine ===")
    demo_bytecode_disassembly()
    demo_compile_vs_exec()
    demo_raw_code_object_bytes()
    demo_pyc_caching()
    print("\nAll CPython & PVM demonstrations completed successfully!")


if __name__ == "__main__":
    main()
