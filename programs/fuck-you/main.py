"""
Fuck You
========
Robot says "fuck you all" every 2 seconds.
Press Ctrl+C to stop.
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

USE_SIM = os.environ.get("REACHY_MINI_SIM", "0") == "1"

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
from shared.tts import say


def get_robot():
    if USE_SIM:
        return ReachyMini(media_backend="no_media")
    else:
        return ReachyMini()


def main():
    print("Press Ctrl+C to stop\n")

    with get_robot() as robot:
        try:
            while True:
                # Aggressive head movement
                robot.goto_target(
                    head=create_head_pose(z=10, roll=0, degrees=True, mm=True),
                    duration=0.2
                )

                say("fuck you all", robot)

                robot.goto_target(
                    head=create_head_pose(z=0, roll=0, degrees=True, mm=True),
                    duration=0.2
                )

                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
