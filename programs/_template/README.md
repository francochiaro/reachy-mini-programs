# Program Template

Copy this template to create new programs that work in both simulator and real robot.

## Usage

```bash
# 1. Copy template
cp -r programs/_template programs/my-program

# 2. Edit your program
# Edit programs/my-program/main.py

# 3. Test in simulator
./run.sh my-program --sim

# 4. Run on real robot
./run.sh my-program
```

## Features

This template handles:

| Feature | Simulator | Real Robot |
|---------|-----------|------------|
| Movement | ✅ Full physics | ✅ Real motors |
| Camera | 📷 Test images | ✅ Live feed |
| Audio output | 🔊 Mac speakers | ✅ Robot speaker |
| Audio input | ⌨️ Simulated | ✅ Robot mics |

## Adding Test Images

For camera testing in simulator, add images to `test_images/`:

```
my-program/
├── main.py
├── test_images/
│   ├── sample1.jpg
│   └── sample2.png
```

The template will automatically use these in simulation mode.

## Helper Functions

```python
# Movement
move_head(robot, z=10, roll=5, duration=0.5)
look_around(robot)
nod_yes(robot)
shake_no(robot)

# Camera (with sim fallback)
frame = get_camera_frame(robot)

# Audio (with sim fallback)
robot_say(robot, "Hello!")
text = listen_for_speech(robot, timeout=5.0)
```
