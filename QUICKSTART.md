# Quick Start Guide

Get your Reachy-Mini running with your programs in minutes.

---

## First-Time Setup (Do Once)

### 1. Clone & Enter Project

```bash
git clone https://github.com/francochiaro/reachy-mini-programs.git
cd reachy-mini-programs
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the Reachy-Mini SDK with MuJoCo simulation support.

---

## Running Programs

### List Available Programs

```bash
./run.sh --list
```

### Run in Simulator (No Robot Needed)

```bash
./run.sh <program-name> --sim
```

### Run on Real Robot

1. **Connect** the USB-C cable from Reachy-Mini to your computer
2. **Wait** for the SDK to auto-discover the robot
3. **Run**:

```bash
./run.sh <program-name>
```

---

## Quick Reference Card

| Command | Description |
|---------|-------------|
| `./run.sh --list` | List all programs |
| `./run.sh <name> --sim` | Run in simulator |
| `./run.sh <name>` | Run on real robot |
| `./run.sh --help` | Show help |

---

## When You Connect the Robot

**Checklist:**

1. [ ] USB-C cable connected
2. [ ] Virtual environment activated: `source venv/bin/activate`
3. [ ] Pick your program: `./run.sh --list`
4. [ ] Run it: `./run.sh <program-name>`

**If something goes wrong:**

- Check USB connection
- Verify robot power
- Try `pip install --upgrade reachy-mini[mujoco]`
- Check the program's README in `programs/<name>/`

---

## Testing in Simulator

Before you have the robot, test everything in the MuJoCo simulator:

```bash
# Test a program
./run.sh wave-hello --sim

# The simulator window will open showing Reachy-Mini
# All movements and behaviors run in physics simulation
```

---

## Creating Your Own Program

```bash
# 1. Create folder
mkdir -p programs/my-program

# 2. Create main.py
cat > programs/my-program/main.py << 'EOF'
import os
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

def main():
    # Connect to robot (or simulator if REACHY_MINI_SIM=1)
    with ReachyMini() as robot:
        # Your program logic here
        robot.goto_target(
            head=create_head_pose(z=10, roll=15, degrees=True, mm=True),
            duration=1.0
        )

if __name__ == "__main__":
    main()
EOF

# 3. Test in simulator
./run.sh my-program --sim
```

---

## Project Structure

```
reachy-mini-programs/
├── run.sh              # <- Your launcher (use this!)
├── requirements.txt    # Dependencies
├── QUICKSTART.md       # This guide
├── REACHY-MINI.md      # Full SDK reference
├── AGENTS.md           # AI agent instructions
└── programs/
    ├── wave-hello/     # Example program
    │   ├── main.py
    │   └── README.md
    └── your-program/   # Your programs go here
        └── main.py
```

---

## Shortcuts Cheat Sheet

Add these to your `~/.bashrc` or `~/.zshrc` for quick access:

```bash
# Quick aliases
alias reachy='cd ~/reachy-mini-programs && source venv/bin/activate'
alias reachy-sim='./run.sh --sim'
alias reachy-list='./run.sh --list'
```

Then just type:
- `reachy` - Jump to project and activate env
- `reachy-list` - See programs
- `reachy-sim wave-hello` - Run in simulator
