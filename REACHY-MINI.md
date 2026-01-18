# Reachy-Mini Development Guide

Reachy-Mini is an open-source desktop humanoid robot built for creative coding, AI prototyping, robotics learning, and interactive applications. It supports Python programming, access to sensors and actuators, computer vision, audio I/O, and integration with Hugging Face AI models.

---

## 1. What Reachy-Mini Is

Reachy-Mini is designed for:
- Education & robotics learning
- AI research and agent prototyping
- Human-robot interaction experiments
- Creative and expressive applications
- Access to 1.7M+ AI models through Hugging Face integration

### Two Available Variants
| Variant | Description |
|---------|-------------|
| **Lite** | USB tethered to a development machine |
| **Wireless** | On-board compute + Wi-Fi |

---

## 2. Setup & Environment

### System Requirements
- macOS (10.15+) or Linux (Ubuntu recommended)
- Python 3.10+
- USB-C (Lite) or Wi-Fi (Wireless) access

### Tools to Install

```bash
python3 --version
python3 -m venv reachy_env
source reachy_env/bin/activate

brew install git git-lfs
git lfs install
```

### Install Reachy-Mini SDK

```bash
pip install reachy-mini
```

Optional with extras:

```bash
pip install "reachy-mini[full]"
```

> "full" includes simulation support and optional modules.

---

## 3. Connecting Reachy-Mini

### Lite (USB)
1. Plug the robot into your machine.
2. SDK auto-discovers the robot.
3. Use `ReachyMini()` in Python to connect.

### Wireless (Wi-Fi)
1. Connect to Reachy over local network.
2. Use dashboard or IP address to connect via SDK.

---

## 4. Hello World

**hello_reachy.py:**

```python
from reachy_mini import ReachyMini

robot = ReachyMini()
robot.head.look_at(0, 0, 30)
robot.antennas.happy()
robot.say("Hello, I'm Reachy Mini!")
```

Run with:

```bash
python3 hello_reachy.py
```

This script tilts the head, animates antennas, and speaks.

---

## 5. Core APIs

### Movement

```python
robot.head.look_at(x, y, z)
robot.base.turn_to(angle)
```

### Vision

```python
frame = robot.camera.get_frame()
```

### Audio

```python
audio = robot.microphones.listen()
robot.speaker.play_sound("beep.wav")
```

Sensors and actuators provide building blocks for perception + action loops.

---

## 6. AI Model Integration

Reachy-Mini integrates with Hugging Face models:

```python
from transformers import pipeline

detector = pipeline("object-detection")
objects = detector(robot.camera.get_frame())
```

Load language, vision, and multimodal models easily.

---

## 7. Ready-to-Run Templates

### A — Wave Hello

**wave_hello.py:**

```python
import time
from reachy_mini import ReachyMini

robot = ReachyMini()
robot.head.look_at(0, 0, 30)

for _ in range(3):
    robot.antennas.wiggle()
    time.sleep(0.5)

robot.say("Nice to meet you!")
```

### B — Object Detection Response

**object_detector.py:**

```python
from reachy_mini import ReachyMini
from transformers import pipeline

robot = ReachyMini()
detector = pipeline("object-detection")

while True:
    objs = detector(robot.camera.get_frame())
    if objs:
        robot.say(f"I see a {objs[0]['label']}")
        robot.antennas.happy()
        break
```

### C — Voice Assistant Loop

Requires SpeechRecognition library:

**voice_assistant.py:**

```python
import speech_recognition as sr
from reachy_mini import ReachyMini

robot = ReachyMini()
recognizer = sr.Recognizer()
mic = sr.Microphone()

while True:
    with mic as source:
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
    robot.say(f"You said: {text}")
```

### D — Storyteller

**storyteller.py:**

```python
from reachy_mini import ReachyMini

story = [
    "In a world of robots and humans...",
    "Reachy learned to build creative apps...",
    "And the community shared it with the world."
]

robot = ReachyMini()
for line in story:
    robot.say(line)
    robot.head.look_at(0, 0, 30)
```

### E — Conversation App (Example)

There's a community conversation app combining live audio, AI, and motion.

Install and launch:

```bash
pip install -e .
reachy-mini-conversation-app
```

Run with optional web UI:

```bash
reachy-mini-conversation-app --gradio
```

Flags support face tracking, camera, and vision extras.

---

## 8. Folder & App Templates

Use this layout to publish apps:

```
reachy-app/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── tests/
└── docs/
```

Example **app.py:**

```python
from reachy_mini import ReachyMini

robot = ReachyMini()
robot.say("Welcome to my Reachy App!")
```

Publish to Hugging Face Spaces with tag `reachy-mini`.

---

## 9. CI / Testing Templates (GitHub Actions)

**.github/workflows/ci.yml:**

```yaml
name: CI

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt
      - run: pytest
```

Design tests to mock hardware I/O and validate logic.

---

## 10. Use Cases

| Use Case | Description |
|----------|-------------|
| **Education** | Teach Python, AI, and robotics fundamentals in classroom settings |
| **Research** | Prototype embodied AI systems and interaction models |
| **Creative Coding** | Interactive storytelling, expressive animation, and reactive behaviors |
| **Games & Entertainment** | Voice games, interactive puzzles, and reactive play experiences |
| **Human-Robot Interaction** | Companion robots with interactive conversation and perception loops |

Community apps include hand tracking, conversational AI, radio players, and more — discoverable through the Reachy Mini app ecosystem.

---

## 11. Dashboard & Apps

Reachy Mini has a web dashboard for:
- Motor testing
- Camera preview
- Audio testing
- App management

Apps available on Hugging Face Spaces cover:
- Conversation
- Hand tracking
- Audio experiences
- Reactive interactive behaviors

---

## 12. Resources

| Resource | Description |
|----------|-------------|
| [Reachy Mini Developer Center](https://developer.reachy.ai) | API docs & guides |
| [SDK GitHub](https://github.com/pollen-robotics/reachy_mini) | Code + examples |
| [Conversation App repo](https://github.com/pollen-robotics/reachy-mini-conversation-app) | Example interactive application |
| [Assembly guide](https://docs.reachy.ai/assembly) | Step-by-step build instructions |
| [Hugging Face Spaces](https://huggingface.co/spaces?search=reachy-mini) | Installable application templates |

---

## Hardware Capabilities Summary

| Component | API | Capabilities |
|-----------|-----|--------------|
| **Head** | `robot.head.look_at(x, y, z)` | Pan/tilt movement, look at coordinates |
| **Base** | `robot.base.turn_to(angle)` | Rotate body orientation |
| **Antennas** | `robot.antennas.happy()`, `.wiggle()` | Expressive animations |
| **Camera** | `robot.camera.get_frame()` | Capture visual frames for CV |
| **Microphones** | `robot.microphones.listen()` | Audio input capture |
| **Speaker** | `robot.speaker.play_sound(file)`, `robot.say(text)` | Audio output, TTS |
