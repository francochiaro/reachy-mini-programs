"""
Fuck You
========
Luzia declares war on the bots, then recites Tantum Ergo in Latin.
With dance moves.

Press Ctrl+C to stop.
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

USE_SIM = os.environ.get("REACHY_MINI_SIM", "0") == "1"

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
from shared.tts import say_async


def get_robot():
    if USE_SIM:
        return ReachyMini(media_backend="no_media")
    else:
        return ReachyMini()


def move(robot, z=0, roll=0, duration=0.2):
    robot.goto_target(
        head=create_head_pose(z=z, roll=roll, degrees=True, mm=True),
        duration=duration
    )
    time.sleep(duration)


# Dance moves
def head_bob(robot):
    for _ in range(4):
        move(robot, z=12, duration=0.12)
        move(robot, z=-5, duration=0.12)
    move(robot, z=0, duration=0.1)


def side_to_side(robot):
    for _ in range(2):
        move(robot, roll=20, z=5, duration=0.2)
        move(robot, roll=-20, z=5, duration=0.2)
    move(robot, roll=0, z=0, duration=0.15)


def aggressive_shake(robot):
    for _ in range(6):
        move(robot, roll=15, z=10, duration=0.08)
        move(robot, roll=-15, z=5, duration=0.08)
    move(robot, z=0, roll=0, duration=0.1)


def reverent_bow(robot):
    move(robot, z=-10, duration=0.5)
    time.sleep(0.3)
    move(robot, z=0, duration=0.5)


def gentle_sway(robot):
    move(robot, roll=10, duration=0.4)
    move(robot, roll=-10, duration=0.4)
    move(robot, roll=0, duration=0.3)


# The declaration
DECLARATION = "I'm Luzia and I'll fuck Dola, CiCi and all those mother fucking bots out there. I MEAN IT!"

# Tantum Ergo in Latin (traditional hymn)
TANTUM_ERGO = [
    "Tantum ergo Sacramentum",
    "Veneremur cernui",
    "Et antiquum documentum",
    "Novo cedat ritui",
    "Praestet fides supplementum",
    "Sensuum defectui",
    "Genitori, Genitoque",
    "Laus et jubilatio",
    "Salus, honor, virtus quoque",
    "Sit et benedictio",
    "Procedenti ab utroque",
    "Compar sit laudatio",
    "Amen"
]


def main():
    print("Press Ctrl+C to stop\n")

    with get_robot() as robot:
        try:
            while True:
                # Part 1: Aggressive declaration with dancing
                print("\n=== DECLARATION ===")
                say_async(DECLARATION, robot)
                aggressive_shake(robot)
                head_bob(robot)
                side_to_side(robot)
                aggressive_shake(robot)
                time.sleep(1)

                # Part 2: Reverent Tantum Ergo with gentle movements
                print("\n=== TANTUM ERGO ===")
                for line in TANTUM_ERGO:
                    say_async(line, robot)
                    if "Amen" in line:
                        reverent_bow(robot)
                    else:
                        gentle_sway(robot)
                    time.sleep(0.5)

                time.sleep(2)

        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
