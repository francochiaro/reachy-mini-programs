"""
Text-to-Speech Helper
=====================
Provides TTS with fallback options:
1. Hugging Face MMS-TTS (best quality, if available)
2. macOS 'say' command (fallback)
"""

import os
import subprocess
import tempfile

USE_SIM = os.environ.get("REACHY_MINI_SIM", "0") == "1"

# Track if HuggingFace TTS is available
_hf_available = None
_hf_model = None
_hf_tokenizer = None


def _check_hf_available():
    """Check if HuggingFace TTS can be loaded."""
    global _hf_available
    if _hf_available is None:
        try:
            from transformers import VitsModel, AutoTokenizer
            _hf_available = True
        except ImportError:
            _hf_available = False
    return _hf_available


def _load_hf_model():
    """Load HuggingFace TTS model."""
    global _hf_model, _hf_tokenizer

    if _hf_model is None:
        print("[TTS] Loading Hugging Face model...")
        from transformers import VitsModel, AutoTokenizer
        _hf_model = VitsModel.from_pretrained('facebook/mms-tts-eng')
        _hf_tokenizer = AutoTokenizer.from_pretrained('facebook/mms-tts-eng')
        print("[TTS] Model ready!")

    return _hf_model, _hf_tokenizer


def _say_with_hf(text):
    """Generate and play speech using HuggingFace."""
    import torch
    import soundfile as sf

    model, tokenizer = _load_hf_model()

    inputs = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        output = model(**inputs).waveform

    # Save and play
    tmp_file = tempfile.mktemp(suffix='.wav')
    sf.write(tmp_file, output.squeeze().numpy(), samplerate=model.config.sampling_rate)
    subprocess.run(['afplay', tmp_file], check=True)
    os.remove(tmp_file)


def _say_with_macos(text, voice="Samantha"):
    """Use macOS built-in TTS."""
    subprocess.run(["say", "-v", voice, text])


def say(text, robot=None, blocking=True):
    """
    Speak text using best available TTS.

    Args:
        text: Text to speak
        robot: ReachyMini instance (for real robot speaker)
        blocking: If True, wait for speech to finish
    """
    print(f"[SAY] {text}")

    try:
        if not USE_SIM and robot is not None:
            # Real robot - use robot speaker
            # First generate audio file, then play on robot
            if _check_hf_available():
                import torch
                import soundfile as sf

                model, tokenizer = _load_hf_model()
                inputs = tokenizer(text, return_tensors='pt')
                with torch.no_grad():
                    output = model(**inputs).waveform

                tmp_file = tempfile.mktemp(suffix='.wav')
                sf.write(tmp_file, output.squeeze().numpy(), samplerate=model.config.sampling_rate)
                robot.media.play_sound(tmp_file)
                os.remove(tmp_file)
            else:
                # Fallback - no TTS available for robot
                print("[TTS] No TTS available for robot")
        else:
            # Simulator - use Mac speakers
            if blocking:
                _say_with_macos(text)
            else:
                subprocess.Popen(["say", text])

    except Exception as e:
        print(f"[TTS] Error: {e}, using fallback")
        subprocess.Popen(["say", text])


def say_async(text, robot=None):
    """Speak without blocking (runs in background thread)."""
    import threading

    def _speak():
        # Use macOS say for async (simpler, avoids threading issues with torch)
        subprocess.run(["say", text])

    print(f"[SAY] {text}")
    thread = threading.Thread(target=_speak)
    thread.daemon = True
    thread.start()
    return thread
