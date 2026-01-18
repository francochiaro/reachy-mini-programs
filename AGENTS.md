# Reachy-Mini Programs - Agent Instructions

## Project Overview

This repository contains **programs/modes** for Reachy-Mini, a desktop humanoid robot by Hugging Face. Each program is a standalone mode that can be loaded onto the robot via USB cable. **Only one program/mode runs at a time.**

## Key Reference

- **REACHY-MINI.md** - Complete SDK documentation, APIs, and hardware capabilities. **Always consult this before implementing any program.**

## Architecture

### Program Structure

Each program is a self-contained Python module that:
1. Initializes a `ReachyMini()` connection
2. Runs a single behavior loop or sequence
3. Uses available hardware: head, antennas, camera, microphones, speaker

### Folder Layout

```
programs/
├── <program-name>/
│   ├── main.py           # Entry point
│   ├── requirements.txt  # Dependencies
│   ├── README.md         # Program description
│   └── tests/            # Unit tests (mock hardware)
```

## Available Hardware APIs

| Component | Methods | Use For |
|-----------|---------|---------|
| `robot.head` | `.look_at(x, y, z)` | Directing attention, tracking |
| `robot.base` | `.turn_to(angle)` | Body orientation |
| `robot.antennas` | `.happy()`, `.wiggle()` | Emotional expression |
| `robot.camera` | `.get_frame()` | Vision input (CV, AI models) |
| `robot.microphones` | `.listen()` | Audio input |
| `robot.speaker` | `.play_sound(file)`, `robot.say(text)` | Audio output, TTS |

## Development Guidelines

### Creating a New Program

1. Create folder under `programs/<program-name>/`
2. Implement `main.py` with `ReachyMini()` initialization
3. Add `requirements.txt` with dependencies
4. Write tests that mock hardware I/O
5. Document in program's `README.md`

### Code Patterns

```python
# Standard program template
from reachy_mini import ReachyMini

def main():
    robot = ReachyMini()

    # Program logic here
    # Use perception -> decision -> action loops

if __name__ == "__main__":
    main()
```

### AI Integration

Programs can use Hugging Face models:

```python
from transformers import pipeline

# Object detection, speech recognition, LLMs, etc.
detector = pipeline("object-detection")
results = detector(robot.camera.get_frame())
```

## Constraints

- **One mode at a time**: Programs are mutually exclusive
- **USB tethered (Lite)**: Most development uses USB connection
- **Python 3.10+**: Required runtime
- **Hardware limits**: Head movement, antenna expressions, single camera, stereo mics, mono speaker

## Testing

- Mock `ReachyMini()` for unit tests
- Test perception logic separately from hardware
- Use pytest with hardware mocking

## Discovered Patterns

*(Add patterns discovered during development here)*

- Keep perception-action loops tight for responsive behavior
- Use `time.sleep()` sparingly; prefer event-driven patterns
- Antenna expressions add personality without complexity
- Camera frames work directly with HuggingFace pipelines

## Commands

```bash
# Install SDK
pip install reachy-mini

# Run a program
python programs/<program-name>/main.py

# Run tests
pytest programs/<program-name>/tests/
```
