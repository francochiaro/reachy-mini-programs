"""
Wave Hello Program
==================
A friendly greeting program where Reachy-Mini waves and says hello.
Works in both simulation and on the real robot.
"""

import time
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose


def wave_sequence(robot):
    """Perform a friendly wave sequence."""
    # Look up and to the side
    robot.goto_target(
        head=create_head_pose(z=15, roll=10, degrees=True, mm=True),
        duration=0.5
    )
    time.sleep(0.3)

    # Wiggle antennas (happy expression)
    for _ in range(3):
        robot.goto_target(
            head=create_head_pose(z=15, roll=-10, degrees=True, mm=True),
            duration=0.2
        )
        time.sleep(0.2)
        robot.goto_target(
            head=create_head_pose(z=15, roll=10, degrees=True, mm=True),
            duration=0.2
        )
        time.sleep(0.2)

    # Return to neutral
    robot.goto_target(
        head=create_head_pose(z=0, roll=0, degrees=True, mm=True),
        duration=0.5
    )


def main():
    print("Starting Wave Hello program...")
    print("Connecting to Reachy-Mini...")

    with ReachyMini() as robot:
        print("Connected! Running wave sequence...")

        # Perform the wave
        wave_sequence(robot)

        print("Wave complete!")
        time.sleep(1.0)


if __name__ == "__main__":
    main()
