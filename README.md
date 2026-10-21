# Python Internals & Mental Models

A foundational curriculum explaining how Python works under the hood—from high-level abstractions and memory management down to CPython compilation, bytecode, and the Python Virtual Machine (PVM).

---

## Table of Contents
1. [Module 1: The Mental Model — Talking to a Machine](#module-1-the-mental-model--talking-to-a-machine)
   - [The Lagos Commute Analogy](#the-lagos-commute-analogy)
   - [Low-Level Languages: Working Close to the Metal](#low-level-languages-working-close-to-the-metal)
   - [Abstraction and Developer Responsibility](#abstraction-and-developer-responsibility)
   - [Python’s Automatic Memory-Management Model](#pythons-automatic-memory-management-model)
   - [Demonstrations in Code](#module-1-code-demonstrations)
2. [Module 2: CPython, Bytecode, and the Python Virtual Machine](#module-2-cpython-bytecode-and-the-python-virtual-machine)
   - [Source Code to Machine Execution](#source-code-to-machine-execution)
   - [CPython: The Reference Implementation](#cpython-the-reference-implementation)
   - [Compilation to Bytecode](#cpython-compilation-to-bytecode)
   - [The Python Virtual Machine (PVM)](#the-python-virtual-machine-pvm)
   - [Why Python is Described as Interpreted](#why-python-is-described-as-interpreted)
   - [The UN Live Interpreter Analogy](#the-un-live-interpreter-analogy)
   - [Life Cycle of a Python Script](#life-cycle-of-a-python-script)
   - [Demonstrations in Code](#module-2-code-demonstrations)
3. [Running the Demonstration Scripts](#running-the-demonstration-scripts)

---

## Module 1: The Mental Model — Talking to a Machine

### The Lagos Commute Analogy
Imagine you are in Lagos and you want to get from Ojota to CMS on the Island. You have two ways to describe the journey:

1. **High-Level Instruction:**
   Tell a professional driver: *"Please take me to CMS. You can use the Third Mainland Bridge or Eko Bridge, depending on traffic."*
   The driver understands this. The driver knows how to operate the accelerator, brake, steering, indicator lights, and gearbox. You do not need to explain how to press the clutch or when to change gear. You are operating at a high level of instruction.

2. **Low-Level Instruction:**
   Do everything yourself. You enter the car, adjust the seat, press the clutch, shift into first gear, check the mirror, release the handbrake, gently press the accelerator, and manage every single physical mechanical action.

Programming languages follow this exact distinction. Some are **high-level**, meaning they hide the messy details of the machine from you. Others are **low-level**, meaning they require you to manage those details directly.

Python is a **high-level language**. It lets you say, *"Take this data to that result,"* without needing to manage every physical detail of the computer’s memory, processor, or operating system.

### Low-Level Languages: Working Close to the Metal
Low-level languages are close to the computer’s hardware:
- **Machine Code:** The lowest level—a stream of binary numbers (`0`s and `1`s) that the processor executes directly.
- **Assembly Language:** Slightly above machine code, using short mnemonics like `MOV`, `ADD`, and `JMP`.

In low-level languages such as C or assembly, the programmer is personally responsible for hardware tasks:
- Allocating memory for a variable.
- Freeing that memory when it is no longer needed.
- Managing how data is stored in specific memory addresses.
- Handling pointer arithmetic.

> **The Yam Trader Analogy:** If you handle every cash transaction manually in a market stall, you know where every single naira note goes. But you also spend extensive time counting, securing, and reconciling cash. If you make a mistake, cash is lost. Low-level programming gives you total control, but also total responsibility.

### Abstraction and Developer Responsibility
**Abstraction** means hiding complexity behind a simpler interface.
A car’s steering wheel is an abstraction: you turn the wheel, and the vehicle turns. You do not need to understand the steering rack, power steering fluid, or tie rods.

In Python:
```python
fruits = ["mango", "pawpaw", "orange", "banana"]
```
You do not have to calculate byte sizes, allocate arrays, or reallocate memory buffers when items are added. Python handles these low-level tasks automatically.

### Python’s Automatic Memory-Management Model
Python frees developers from manual memory management through two coordinated mechanisms:
1. **Reference Counting (Immediate):** Python tracks the number of variables pointing to an object. As soon as that reference count hits 0, memory is released immediately.
2. **Cycle-Detecting Garbage Collector (Scheduled):** A background sweeper ("house help") that runs periodically to detect and clean circular references where objects reference each other.

> **The Market Stall Analogy:** In low-level languages, you rent a shop in a busy market and must personally cancel the lease when you leave; forgetting to vacate means you keep paying rent indefinitely (a memory leak). In Python, market management automatically repossesses and cleans the stall once you vacate it.

### Module 1 Code Demonstrations
Run the companion script [`memory_model_demo.py`](memory_model_demo.py) to see:
- Dynamic memory expansion (`sys.getsizeof`)
- Variables as labels vs. memory addresses (`id()`, `is`)
- Reference counting & immediate deallocation (`sys.getrefcount`, `__del__`)
- Resolving circular references with `gc.collect()`

---

## Module 2: CPython, Bytecode, and the Python Virtual Machine

### Source Code to Machine Execution
When you write Python, you create a human-readable text file (e.g., `pay.py`):
```python
balance = 10000
withdrawal = 3000
balance = balance - withdrawal
print(balance)
```
A computer processor cannot execute this text directly. It requires machine code. The translator that bridges this gap is the Python interpreter.

### CPython: The Reference Implementation
When people refer to "Python", they usually mean **CPython**—the standard, default implementation written in C (from python.org). Other implementations include PyPy (JIT compiler), Jython (runs on JVM), and IronPython (.NET).

CPython executes your program in two distinct stages:
1. **Compile** Python source code into platform-independent **bytecode**.
2. **Execute** that bytecode on the **Python Virtual Machine (PVM)**.

### CPython Compilation to Bytecode
Before executing, CPython compiles `.py` source text into **bytecode** (often cached in `__pycache__/*.pyc`).
Bytecode is not processor machine code; it is an intermediate instruction set designed specifically for the Python Virtual Machine.

Conceptually, our arithmetic code compiles into bytecode instructions:
```text
LOAD_NAME balance
LOAD_NAME withdrawal
BINARY_OP subtract
STORE_NAME balance
LOAD_NAME print
LOAD_NAME balance
CALL 1
```

### The Python Virtual Machine (PVM)
The PVM is the runtime engine within CPython that reads bytecode instructions sequentially and performs the actual machine operations (evaluating arithmetic, allocating objects, invoking system calls).

### Why Python is Described as Interpreted
Python is called interpreted because its bytecode requires the Python runtime/PVM to execute, rather than compiling down to a standalone native binary like C or Rust. Compilation to bytecode is an internal execution stage, not an external build step.

### The UN Live Interpreter Analogy
- **Compiling to Native Code (C / Go):** Transcribing a speech once into a printed book. Readers can read the book anywhere without a translator present.
- **Python's Model:** Recording a speech (bytecode) and playing it back with an interpreter translating live into the listener's earpiece (the PVM). You always need the runtime to execute the program.

### Life Cycle of a Python Script
1. You run `python pay.py`.
2. CPython reads `pay.py`.
3. If no valid cache exists in `__pycache__/`, CPython compiles `pay.py` into bytecode.
4. CPython caches the bytecode in `__pycache__/pay.cpython-<version>.pyc`.
5. The PVM steps through the bytecode instructions sequentially.
6. The program completes and exits.

### Module 2 Code Demonstrations
Run the companion script [`cpython_bytecode_demo.py`](cpython_bytecode_demo.py) to see:
- Real CPython bytecode disassembly using `dis.dis()`
- Proof of two-stage execution using `compile()` and `exec()`
- Internal code object byte inspection (`co_code`, `co_consts`, `co_names`)
- Bytecode compilation and `.pyc` cache inspection (`py_compile`)

---

## Running the Demonstration Scripts

Clone the repository and run both modules directly in any standard Python 3 environment:

```bash
# Run Module 1: Memory management, abstraction & garbage collection
python3 memory_model_demo.py

# Run Module 2: CPython compilation, bytecode disassembly & PVM execution
python3 cpython_bytecode_demo.py
```
