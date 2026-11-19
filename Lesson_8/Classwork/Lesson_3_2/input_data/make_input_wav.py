# python Lesson_3/2/input_data/make_input_wav.py

import math
import struct
import wave
from pathlib import Path

TARGET = Path("Lesson_3/2/input_data/input.wav")

SAMPLE_RATE = 44100
DURATION = 5.0
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16-bit PCM


def main():
    TARGET.parent.mkdir(parents=True, exist_ok=True)

    n = int(SAMPLE_RATE * DURATION)
    frames = bytearray()
    max16 = 32767.0

    for i in range(n):
        t = i / SAMPLE_RATE

        # Несколько гармоник
        x = (
            0.55 * math.sin(2 * math.pi * 0.0055 * t)
            + 0.55 * math.sin(2 * math.pi * 220 * t)
            + 0.25 * math.sin(2 * math.pi * 440 * t)
            + 0.72 * math.sin(2 * math.pi * 990 * t)
            + 0.05 * math.sin(2 * math.pi * 3910 * t)
        )

        '''
        # Несколько гармоник
        x = (
            0.55 * math.sin(2 * math.pi * 220 * t)
            + 0.25 * math.sin(2 * math.pi * 440 * t)
            + 0.12 * math.sin(2 * math.pi * 990 * t)
            + 0.05 * math.sin(2 * math.pi * 3910 * t)
        )
        '''

        x = max(-1.0, min(1.0, x))
        sample = int(x * max16)
        frames += struct.pack("<h", sample)

    with wave.open(str(TARGET), "wb") as wav:
        wav.setnchannels(CHANNELS)
        wav.setsampwidth(SAMPLE_WIDTH)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(bytes(frames))

    print(f"Создан WAV-файл: {TARGET.resolve()}")


if __name__ == "__main__":
    main()