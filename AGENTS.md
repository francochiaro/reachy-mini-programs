# Reachy-Mini Programs - Agent Instructions

## Project Overview

This repository contains **programs/modes** for Reachy-Mini, a desktop humanoid robot by Hugging Face/Pollen Robotics. Each program is a standalone mode that runs on the robot via USB cable. **Only one program/mode runs at a time.**

## Key References

- **REACHY-MINI.md** - Complete SDK documentation, APIs, and hardware capabilities
- **QUICKSTART.md** - User guide for running programs on robot or simulator

## Project Structure

```
reachy-mini-programs/
├── run.sh              # Launcher script (main entry point)
├── requirements.txt    # SDK + simulation dependencies
├── QUICKSTART.md       # User quick-start guide
├── REACHY-MINI.md      # Full SDK reference
├── AGENTS.md           # This file (AI agent instructions)
└── programs/
    └── <program-name>/
        ├── main.py           # Entry point (required)
        ├── requirements.txt  # Program-specific deps (optional)
        └── README.md         # Program description
```

## Running Programs

```bash
# List available programs
./run.sh --list

# Run in MuJoCo simulator
./run.sh <program-name> --sim

# Run on real robot (USB connected)
./run.sh <program-name>
```

## Available Hardware APIs

| Component | Methods | Use For |
|-----------|---------|---------|
| `robot.goto_target()` | `head=create_head_pose(...)` | Head movement with duration |
| `robot.head` | `.look_at(x, y, z)` | Directing attention, tracking |
| `robot.base` | `.turn_to(angle)` | Body orientation |
| `robot.antennas` | `.happy()`, `.wiggle()` | Emotional expression |
| `robot.camera` | `.get_frame()` | Vision input (CV, AI models) |
| `robot.microphones` | `.listen()` | Audio input |
| `robot.speaker` | `.play_sound(file)`, `robot.say(text)` | Audio output, TTS |

## Creating a New Program

### 1. Create the folder structure

```bash
mkdir -p programs/<program-name>
```

### 2. Implement main.py

```python
"""
Program Name
============
Brief description of what this program does.
"""

import time
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose


def main():
    print("Starting program...")

    with ReachyMini() as robot:
        # Your program logic here
        robot.goto_target(
            head=create_head_pose(z=10, roll=0, degrees=True, mm=True),
            duration=1.0
        )

        # Keep robot active or loop as needed
        time.sleep(1.0)


if __name__ == "__main__":
    main()
```

### 3. Add README.md

```markdown
# Program Name

Brief description.

## What It Does

- Step 1
- Step 2

## Run

\`\`\`bash
./run.sh <program-name> --sim   # Simulator
./run.sh <program-name>          # Real robot
\`\`\`
```

### 4. Test in simulator

```bash
./run.sh <program-name> --sim
```

## Code Patterns

### Use Context Manager

Always use `with ReachyMini() as robot:` to ensure proper cleanup:

```python
with ReachyMini() as robot:
    # robot is automatically connected and cleaned up
    pass
```

### Head Movement with Duration

Use `goto_target` with `create_head_pose` for smooth movements:

```python
from reachy_mini.utils import create_head_pose

robot.goto_target(
    head=create_head_pose(z=15, roll=10, degrees=True, mm=True),
    duration=0.5  # seconds
)
```

### AI Model Integration

```python
from transformers import pipeline

detector = pipeline("object-detection")

with ReachyMini() as robot:
    frame = robot.camera.get_frame()
    results = detector(frame)
```

## Constraints

- **One mode at a time**: Programs are mutually exclusive
- **USB tethered (Lite)**: Primary development mode
- **Python 3.10+**: Required runtime
- **MuJoCo simulation**: Use `--sim` flag to test without hardware

## Testing Strategy

1. **Always test in simulator first**: `./run.sh <name> --sim`
2. **Mock hardware for unit tests**: Create mock ReachyMini class
3. **Test perception logic separately**: Process sample frames offline

## Commands Reference

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run programs
./run.sh --list                    # List all programs
./run.sh <program-name> --sim      # Simulator
./run.sh <program-name>            # Real robot

# Development
pytest programs/<name>/tests/      # Run tests
```

## Discovered Patterns

- Use `with ReachyMini()` context manager for clean connections
- `goto_target()` with duration creates smooth, natural movements
- Keep perception-action loops tight for responsive behavior
- Test everything in simulator before real robot
- Antenna expressions add personality without complexity
- Camera frames work directly with HuggingFace pipelines
