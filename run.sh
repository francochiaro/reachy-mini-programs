#!/bin/bash
# Reachy-Mini Program Launcher
# Usage: ./run.sh <program-name> [--sim]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROGRAMS_DIR="$SCRIPT_DIR/programs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_help() {
    echo -e "${BLUE}Reachy-Mini Program Launcher${NC}"
    echo ""
    echo "Usage: ./run.sh <program-name> [options]"
    echo ""
    echo "Options:"
    echo "  --sim       Run in simulation mode (MuJoCo)"
    echo "  --list      List available programs"
    echo "  --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run.sh wave-hello          # Run on real robot"
    echo "  ./run.sh wave-hello --sim    # Run in simulator"
    echo "  ./run.sh --list              # List all programs"
}

list_programs() {
    echo -e "${BLUE}Available Programs:${NC}"
    echo ""
    if [ -d "$PROGRAMS_DIR" ]; then
        for dir in "$PROGRAMS_DIR"/*/; do
            if [ -f "${dir}main.py" ]; then
                name=$(basename "$dir")
                desc=""
                if [ -f "${dir}README.md" ]; then
                    desc=$(head -n 3 "${dir}README.md" | grep -v "^#" | grep -v "^$" | head -n 1)
                fi
                echo -e "  ${GREEN}$name${NC}"
                [ -n "$desc" ] && echo "    $desc"
            fi
        done
    else
        echo -e "  ${YELLOW}No programs found. Create one in programs/<name>/main.py${NC}"
    fi
    echo ""
}

run_program() {
    local program="$1"
    local sim_mode="$2"
    local program_dir="$PROGRAMS_DIR/$program"
    local main_file="$program_dir/main.py"

    if [ ! -d "$program_dir" ]; then
        echo -e "${RED}Error: Program '$program' not found${NC}"
        echo "Run './run.sh --list' to see available programs"
        exit 1
    fi

    if [ ! -f "$main_file" ]; then
        echo -e "${RED}Error: No main.py found in $program_dir${NC}"
        exit 1
    fi

    # Check for program-specific requirements
    if [ -f "$program_dir/requirements.txt" ]; then
        echo -e "${YELLOW}Installing program dependencies...${NC}"
        pip install -q -r "$program_dir/requirements.txt"
    fi

    # Set simulation environment variable if requested
    if [ "$sim_mode" = "true" ]; then
        echo -e "${BLUE}Starting in SIMULATION mode...${NC}"
        export REACHY_MINI_SIM=1
    else
        echo -e "${GREEN}Starting on REAL ROBOT...${NC}"
        export REACHY_MINI_SIM=0
    fi

    echo -e "Running: ${GREEN}$program${NC}"
    echo "----------------------------------------"

    # Run the program
    python "$main_file"
}

# Parse arguments
PROGRAM=""
SIM_MODE="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --sim)
            SIM_MODE="true"
            shift
            ;;
        --list)
            list_programs
            exit 0
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        -*)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
        *)
            PROGRAM="$1"
            shift
            ;;
    esac
done

if [ -z "$PROGRAM" ]; then
    show_help
    exit 0
fi

run_program "$PROGRAM" "$SIM_MODE"
