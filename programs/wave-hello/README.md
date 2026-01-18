# Wave Hello

A friendly greeting program where Reachy-Mini performs a wave and says hello.

## What It Does

1. Looks up and tilts head to the side
2. Performs a wiggling wave motion (3 times)
3. Returns to neutral position

## Run

```bash
# Simulator
./run.sh wave-hello --sim

# Real robot
./run.sh wave-hello
```

## Customization

Edit `main.py` to change:
- Wave speed (adjust `duration` parameters)
- Number of wiggles (change the loop count)
- Head angles (modify `z` and `roll` values)
