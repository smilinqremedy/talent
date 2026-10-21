#!/usr/bin/env bash
# ==============================================================================
# The Computer Has a Manager: The Kernel, The Shell, and The Terminal
# Hands-on demonstrations showing:
# 1. Inspecting the Kernel vs. the Shell.
# 2. How the Shell resolves and runs commands via $PATH.
# 3. The Abuja Data Analyst automation scenario (batch processing files).
# 4. Bash as a full programmable environment (variables, logic, arithmetic).
# ==============================================================================

set -e

banner() {
    echo ""
    echo "================================================================="
    echo " $1"
    echo "================================================================="
    echo ""
}

# ------------------------------------------------------------------------------
# Demo 1: The Manager (Kernel) vs. The Front Desk (Shell)
# ------------------------------------------------------------------------------
demo_kernel_vs_shell() {
    banner "Demo 1: The Manager (Kernel) vs. The Front Desk (Shell)"
    echo "The Kernel manages memory, processes, and hardware."
    echo "The Shell interprets text commands and communicates with the Kernel."
    echo ""

    echo "1. Kernel Information (queried via uname system call):"
    echo "   OS Name        : $(uname -s)"
    echo "   Kernel Release : $(uname -r)"
    echo "   Architecture   : $(uname -m)"
    echo ""

    echo "2. Shell Information (queried from active shell process):"
    echo "   Shell Program  : $SHELL"
    echo "   Shell Process ID: $$"
    echo "   Bash Version   : ${BASH_VERSION:-'Non-bash subshell'}"
    echo ""
    echo "Takeaway: uname talks to the kernel manager; \$SHELL and \$\$ are shell state."
}

# ------------------------------------------------------------------------------
# Demo 2: Under the Hood of a Command ($PATH & REPL)
# ------------------------------------------------------------------------------
demo_path_and_repl() {
    banner "Demo 2: How the Shell Finds Commands (\$PATH)"
    echo "When you type 'ls', the shell does not guess."
    echo "It searches directories listed in your \$PATH variable sequentially:\n"

    echo "1. Binary location for 'ls':"
    which ls || true
    echo ""

    echo "2. Binary location for 'python3':"
    which python3 || true
    echo ""

    echo "3. System \$PATH search locations:"
    echo "$PATH" | tr ':' '\n' | sed 's/^/   -> /'

    echo ""
    echo "Takeaway: The REPL reads 'ls', finds /usr/bin/ls in \$PATH, asks the kernel"
    echo "to fork and execute the program, prints the result, and loops back."
}

# ------------------------------------------------------------------------------
# Demo 3: The Abuja Data Analyst (Batch File Processing)
# ------------------------------------------------------------------------------
demo_abuja_analyst() {
    banner "Demo 3: The Abuja Data Analyst (Batch Automation in Action)"
    echo "Processing 2,000 files with a mouse takes hours."
    echo "With a shell loop, thousands of files can be processed in seconds.\n"

    TMP_DIR=$(mktemp -d /tmp/abuja_sales_XXXXXX)

    echo "1. Generating simulated daily sales files..."
    echo "tx_id,amount,status" > "$TMP_DIR/day_1.csv"
    echo "1001,45000,SUCCESS" >> "$TMP_DIR/day_1.csv"
    echo "1002,12000,SUCCESS" >> "$TMP_DIR/day_1.csv"

    echo "tx_id,amount,status" > "$TMP_DIR/day_2.csv"
    echo "1003,98000,SUCCESS" >> "$TMP_DIR/day_2.csv"

    echo "tx_id,amount,status" > "$TMP_DIR/day_3.csv"
    echo "1004,150000,FLAGGED" >> "$TMP_DIR/day_3.csv"

    echo "Created sample CSVs in $TMP_DIR:"
    ls -l "$TMP_DIR"

    echo ""
    echo "2. Running automated batch extraction loop:"
    for file in "$TMP_DIR"/*.csv; do
        filename=$(basename "$file")
        record_count=$(tail -n +2 "$file" | wc -l)
        echo "   [Extracted] $filename has $record_count transaction records."
    done

    # Clean up
    rm -rf "$TMP_DIR"
    echo ""
    echo "Takeaway: Shell loops turn hours of manual clicking into a 3-line script."
}

# ------------------------------------------------------------------------------
# Demo 4: Bash as a Programmable Environment
# ------------------------------------------------------------------------------
demo_programmable_shell() {
    banner "Demo 4: Bash is a Full Programming Environment"
    echo "Bash supports variables, arithmetic, conditions, and functions.\n"

    WORKSHOP="Lagos Mechanic Hub"
    RECOMMENDED_PSI=32
    CURRENT_PSI=27

    echo "Workshop Name : $WORKSHOP"
    echo "Target PSI    : $RECOMMENDED_PSI"
    echo "Current PSI   : $CURRENT_PSI"
    echo ""

    if [ "$CURRENT_PSI" -lt "$RECOMMENDED_PSI" ]; then
        DEFICIT=$((RECOMMENDED_PSI - CURRENT_PSI))
        echo "Action required: Tire pressure is low by $DEFICIT PSI. Pumping air..."
    else
        echo "Status: Tire pressure is optimal."
    fi

    echo ""
    echo "Takeaway: Bash scripts combine system commands with algorithmic logic."
}

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
main() {
    echo "=== The Computer Has a Manager: Kernel, Shell, and Terminal ==="
    demo_kernel_vs_shell
    demo_path_and_repl
    demo_abuja_analyst
    demo_programmable_shell
    echo ""
    echo "All shell and kernel demonstrations completed successfully!"
}

main "$@"
