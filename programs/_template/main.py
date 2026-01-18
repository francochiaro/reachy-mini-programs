"""
Program Template
================
Copy this template to create new programs.
Handles both simulation and real robot modes gracefully.

Usage:
    1. Copy this folder: cp -r programs/_template programs/my-program
    2. Edit main.py with your logic
    3. Run: ./run.sh my-program --sim
"""

import os
import time
from pathlib import Path

# Detect simulation mode early
USE_SIM = os.environ.get("REACHY_MINI_SIM", "0") == "1"

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

# Optional: for camera/vision programs
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False


# =============================================================================
# CONFIGURATION
# =============================================================================

PROGRAM_DIR = Path(__file__).parent
TEST_IMAGES_DIR = PROGRAM_DIR / "test_images"


# =============================================================================
# ROBOT CONNECTION
# =============================================================================

def get_robot():
    """
    Connect to robot or simulator.

    In simulation: disables camera to avoid errors
    On real robot: full media access
    """
    if USE_SIM:
        print("[SIM] Connecting to simulator...")
        return ReachyMini(media_backend="no_media")
    else:
        print("[ROBOT] Connecting to real robot...")
        return ReachyMini()


# =============================================================================
# CAMERA HELPERS
# =============================================================================

def get_camera_frame(robot):
    """
    Get a camera frame, with simulation fallback.

    In simulation: returns a test image (or None if no test images)
    On real robot: returns live camera frame
    """
    if USE_SIM:
        return _get_test_image()
    else:
        return robot.camera.get_frame()


def _get_test_image():
    """Load a test image for simulation mode."""
    if not HAS_CV2:
        print("[SIM] OpenCV not available, skipping camera")
        return None

    # Look for test images
    if TEST_IMAGES_DIR.exists():
        images = list(TEST_IMAGES_DIR.glob("*.jpg")) + \
                 list(TEST_IMAGES_DIR.glob("*.png"))
        if images:
            img = cv2.imread(str(images[0]))
            print(f"[SIM] Using test image: {images[0].name}")
            return img

    # Create a dummy colored image if no test images
    if HAS_NUMPY:
        print("[SIM] No test images found, using dummy frame")
        return np.zeros((480, 640, 3), dtype=np.uint8)

    return None


# =============================================================================
# AUDIO HELPERS
# =============================================================================

def robot_say(robot, text):
    """
    Make robot speak, with simulation feedback.

    In simulation: prints to console (audio may still play via Mac speakers)
    On real robot: speaks through robot speaker
    """
    print(f"[SPEECH] {text}")

    # robot.say() may work in sim mode using Mac speakers
    # Wrap in try/except in case it fails
    try:
        # Uncomment if you want audio in sim mode too:
        # robot.say(text)
        if not USE_SIM:
            robot.say(text)
    except Exception as e:
        print(f"[AUDIO ERROR] {e}")


def listen_for_speech(robot, timeout=5.0):
    """
    Listen for speech input.

    In simulation: returns dummy text (or uses Mac mic if available)
    On real robot: uses robot microphones
    """
    if USE_SIM:
        print(f"[SIM] Simulating speech input (waiting {timeout}s)...")
        time.sleep(min(timeout, 1.0))  # Shorter wait in sim
        return "[simulated speech input]"
    else:
        audio = robot.microphones.listen(timeout=timeout)
        # Process audio with speech recognition here
        return audio


# =============================================================================
# MOVEMENT HELPERS
# =============================================================================

def move_head(robot, z=0, roll=0, pitch=0, duration=0.5):
    """
    Move robot head to position.

    Args:
        z: Height in mm (positive = up)
        roll: Tilt left/right in degrees (positive = right)
        pitch: Tilt forward/back in degrees (positive = forward)
        duration: Time to reach position in seconds
    """
    robot.goto_target(
        head=create_head_pose(z=z, roll=roll, degrees=True, mm=True),
        duration=duration
    )
    time.sleep(duration + 0.1)  # Wait for movement to complete


def look_around(robot):
    """Example: Make robot look around."""
    print("Looking around...")
    move_head(robot, z=10, roll=20, duration=0.4)   # Look right
    move_head(robot, z=10, roll=-20, duration=0.4)  # Look left
    move_head(robot, z=0, roll=0, duration=0.3)     # Center


def nod_yes(robot):
    """Example: Nod head yes."""
    print("Nodding yes...")
    for _ in range(2):
        move_head(robot, z=15, duration=0.2)
        move_head(robot, z=-5, duration=0.2)
    move_head(robot, z=0, duration=0.2)


def shake_no(robot):
    """Example: Shake head no."""
    print("Shaking no...")
    for _ in range(2):
        move_head(robot, roll=15, duration=0.15)
        move_head(robot, roll=-15, duration=0.15)
    move_head(robot, roll=0, duration=0.2)


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    """
    Main program logic.
    Modify this function for your specific program.
    """
    mode = "SIMULATOR" if USE_SIM else "REAL ROBOT"
    print(f"=" * 50)
    print(f"Starting Program Template [{mode}]")
    print(f"=" * 50)

    with get_robot() as robot:
        print("Connected!")

        # ----- YOUR PROGRAM LOGIC GOES HERE -----

        # Example: Movement
        print("\n--- Movement Demo ---")
        look_around(robot)
        nod_yes(robot)

        # Example: Camera (with sim fallback)
        print("\n--- Camera Demo ---")
        frame = get_camera_frame(robot)
        if frame is not None:
            print(f"Got frame: {frame.shape}")
        else:
            print("No camera frame available")

        # Example: Speech
        print("\n--- Speech Demo ---")
        robot_say(robot, "Hello! I am Reachy Mini.")

        # ----- END OF YOUR LOGIC -----

        print("\nProgram complete!")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
