"""
Dance Party
===========
Reachy-Mini dances and sings in an infinite loop!
Each cycle is ~5 seconds.

Press Ctrl+C to stop.
"""

import os
import time
import random

USE_SIM = os.environ.get("REACHY_MINI_SIM", "0") == "1"

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose


def get_robot():
    if USE_SIM:
        print("[SIM] Connecting to simulator...")
        return ReachyMini(media_backend="no_media")
    else:
        print("[ROBOT] Connecting to real robot...")
        return ReachyMini()


def move(robot, z=0, roll=0, duration=0.2):
    """Quick move helper."""
    robot.goto_target(
        head=create_head_pose(z=z, roll=roll, degrees=True, mm=True),
        duration=duration
    )
    time.sleep(duration)


def say(robot, text):
    """Say something (works in sim and real)."""
    print(f"  {text}")
    # Use Mac's text-to-speech in simulation, robot speaker on real robot
    try:
        if USE_SIM:
            # Use macOS built-in text-to-speech
            import subprocess
            subprocess.Popen(["say", text])
        else:
            robot.say(text)
    except:
        pass


# =============================================================================
# DANCE MOVES (each ~1 second)
# =============================================================================

def head_bob(robot):
    """Bob head up and down to the beat."""
    for _ in range(4):
        move(robot, z=12, duration=0.12)
        move(robot, z=-5, duration=0.12)
    move(robot, z=0, duration=0.1)


def side_to_side(robot):
    """Sway side to side."""
    for _ in range(2):
        move(robot, roll=20, z=5, duration=0.2)
        move(robot, roll=-20, z=5, duration=0.2)
    move(robot, roll=0, z=0, duration=0.15)


def wiggle(robot):
    """Quick wiggles."""
    for _ in range(6):
        move(robot, roll=12, duration=0.08)
        move(robot, roll=-12, duration=0.08)
    move(robot, roll=0, duration=0.1)


def look_up_down(robot):
    """Look up then down dramatically."""
    move(robot, z=20, duration=0.25)
    time.sleep(0.1)
    move(robot, z=-10, duration=0.25)
    time.sleep(0.1)
    move(robot, z=0, duration=0.2)


def circle_head(robot):
    """Move head in a circle pattern."""
    positions = [
        (10, 15),   # up-right
        (-5, 15),   # down-right
        (-5, -15),  # down-left
        (10, -15),  # up-left
    ]
    for z, roll in positions:
        move(robot, z=z, roll=roll, duration=0.18)
    move(robot, z=0, roll=0, duration=0.15)


def excited_shake(robot):
    """Excited fast shaking."""
    for _ in range(8):
        move(robot, roll=8, z=8, duration=0.05)
        move(robot, roll=-8, z=5, duration=0.05)
    move(robot, z=0, roll=0, duration=0.1)


# =============================================================================
# SONG LYRICS
# =============================================================================

LYRICS = [
    "La la la!",
    "Yeah yeah yeah!",
    "Dance with me!",
    "Woo hoo!",
    "I love to dance!",
    "Beep boop beep!",
    "Robot groove!",
    "Let's go!",
    "Oh yeah!",
    "Feeling good!",
]


# =============================================================================
# DANCE ROUTINES (~5 seconds each)
# =============================================================================

def dance_routine_1(robot):
    """Routine 1: Classic dance."""
    say(robot, random.choice(LYRICS))
    head_bob(robot)
    side_to_side(robot)
    wiggle(robot)
    time.sleep(0.2)


def dance_routine_2(robot):
    """Routine 2: Dramatic dance."""
    say(robot, random.choice(LYRICS))
    look_up_down(robot)
    circle_head(robot)
    head_bob(robot)
    time.sleep(0.2)


def dance_routine_3(robot):
    """Routine 3: Energetic dance."""
    say(robot, random.choice(LYRICS))
    excited_shake(robot)
    side_to_side(robot)
    wiggle(robot)
    time.sleep(0.2)


def dance_routine_4(robot):
    """Routine 4: Smooth dance."""
    say(robot, random.choice(LYRICS))
    circle_head(robot)
    side_to_side(robot)
    look_up_down(robot)
    time.sleep(0.2)


ROUTINES = [
    dance_routine_1,
    dance_routine_2,
    dance_routine_3,
    dance_routine_4,
]


# =============================================================================
# MAIN
# =============================================================================

def main():
    mode = "SIMULATOR" if USE_SIM else "REAL ROBOT"
    print("=" * 50)
    print(f"   DANCE PARTY [{mode}]")
    print("=" * 50)
    print("Press Ctrl+C to stop\n")

    with get_robot() as robot:
        print("Let's dance!\n")
        say(robot, "Let's dance!")
        time.sleep(0.5)

        cycle = 0
        try:
            while True:
                cycle += 1
                print(f"--- Cycle {cycle} ---")

                # Pick a random routine
                routine = random.choice(ROUTINES)
                routine(robot)

        except KeyboardInterrupt:
            print("\n\nDance party over!")
            say(robot, "That was fun!")
            move(robot, z=0, roll=0, duration=0.3)
            print("Goodbye!")


if __name__ == "__main__":
    main()
