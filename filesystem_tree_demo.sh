#!/usr/bin/env bash
# ==============================================================================
# The File System is a Tree: Paths, Navigation, and Working Directories
# Hands-on demonstrations showing:
# 1. The Lagos Estate tree structure & pwd.
# 2. Absolute vs. Relative paths (and why context matters).
# 3. Special symbols . (here) and .. (parent directory).
# 4. The Home directory (~) vs. The Root (/).
# ==============================================================================

set -e

banner() {
    echo ""
    echo "================================================================="
    echo " $1"
    echo "================================================================="
    echo ""
}

ESTATE_DIR="/tmp/lagos_estate_demo"
rm -rf "$ESTATE_DIR"
mkdir -p "$ESTATE_DIR/adeola_odeku_st/house_15/room_1"
mkdir -p "$ESTATE_DIR/victoria_island"
echo "Confidential Lagos Business Report" > "$ESTATE_DIR/adeola_odeku_st/house_15/room_1/report.txt"

# ------------------------------------------------------------------------------
# Demo 1: The Lagos Estate Hierarchy & pwd
# ------------------------------------------------------------------------------
demo_estate_hierarchy() {
    banner "Demo 1: The Lagos Estate Hierarchy & pwd"
    echo "The filesystem is an upside-down tree with '/' at the top."
    echo "Root = Main Gate | Directories = Streets/Houses | Files = Documents\n"

    cd "$ESTATE_DIR/adeola_odeku_st/house_15"
    echo "Navigated into house_15."
    echo "Where am I currently standing (pwd)?"
    echo "  Current Working Directory: $(pwd)"
    echo ""
    echo "Takeaway: pwd prints the absolute path of your current shell location."
}

# ------------------------------------------------------------------------------
# Demo 2: Absolute vs. Relative Paths
# ------------------------------------------------------------------------------
demo_absolute_vs_relative() {
    banner "Demo 2: Absolute vs. Relative Paths"
    echo "Absolute: Full address from the root '/' (e.g. Maitama, Abuja address)."
    echo "Relative: Directions from current location (e.g. 'turn into room on right').\n"

    cd "$ESTATE_DIR/adeola_odeku_st/house_15"
    echo "Current directory: $(pwd)"

    echo ""
    echo "1. Reading via RELATIVE path (room_1/report.txt):"
    cat "room_1/report.txt"

    echo ""
    echo "2. Reading via ABSOLUTE path ($ESTATE_DIR/adeola_odeku_st/house_15/room_1/report.txt):"
    cat "$ESTATE_DIR/adeola_odeku_st/house_15/room_1/report.txt"

    echo ""
    echo "3. Moving to a different directory (/tmp) and retrying relative path:"
    cd /tmp
    echo "New working directory: $(pwd)"
    if cat "room_1/report.txt" 2>/dev/null; then
        echo "Success"
    else
        echo "  -> Error: cat: room_1/report.txt: No such file or directory"
        echo "  (Relative paths fail when you are not standing in the expected location!)"
    fi

    echo ""
    echo "Takeaway: Absolute paths work from anywhere; relative paths depend on pwd."
}

# ------------------------------------------------------------------------------
# Demo 3: Navigating with . (Here) and .. (Parent)
# ------------------------------------------------------------------------------
demo_dot_and_dotdot() {
    banner "Demo 3: The Special Symbols . (Here) and .. (One Level Up)"
    echo ".  means 'this current directory' (here)."
    echo ".. means 'parent directory' (one level up toward root).\n"

    cd "$ESTATE_DIR/adeola_odeku_st/house_15/room_1"
    echo "Starting location: $(pwd)"

    echo ""
    echo "1. Using 'cd .' (staying in place):"
    cd .
    echo "  Location after 'cd .' : $(pwd)"

    echo ""
    echo "2. Using 'cd ..' (moving up to house_15):"
    cd ..
    echo "  Location after 'cd ..' : $(pwd)"

    echo ""
    echo "3. Chaining 'cd ../..' (moving two levels up to estate root):"
    cd ../..
    echo "  Location after 'cd ../..': $(pwd)"

    echo ""
    echo "Takeaway: Use .. to step outward; use . to explicitly reference local scripts (./script.sh)."
}

# ------------------------------------------------------------------------------
# Demo 4: The Home Directory (~) vs. Root (/)
# ------------------------------------------------------------------------------
demo_home_vs_root() {
    banner "Demo 4: The Home Directory (~) vs. Root (/)"
    echo "A common beginner mistake is confusing ~ with /."
    echo ""

    echo "1. Navigating to ROOT (/):"
    cd /
    echo "  Location: $(pwd) (The top of the entire hard drive)"
    echo "  Top-level system directories:"
    echo "   " $(ls -d */ | head -n 6)

    echo ""
    echo "2. Navigating to HOME (~):"
    cd ~
    echo "  Location: $(pwd) (Your personal user account space)"

    echo ""
    echo "Takeaway: '/' is shared system space; '~' is your personal workspace."
}

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
main() {
    echo "=== The File System is a Tree: Paths and Navigation ==="
    demo_estate_hierarchy
    demo_absolute_vs_relative
    demo_dot_and_dotdot
    demo_home_vs_root

    # Clean up demo files
    rm -rf "$ESTATE_DIR"
    echo ""
    echo "All filesystem tree demonstrations completed successfully!"
}

main "$@"
