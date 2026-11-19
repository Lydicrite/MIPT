from dataclasses import dataclass
import wave

from histogram import count_levels


@dataclass
class AudioData:
    samples: list[int]
    channels: int
    sample_rate: int
    sample_width: int


def validate_audio(audio):
    if audio.sample_width not in (1, 2, 3, 4):
        raise ValueError("Только 8-, 16-, 24- и 32-битный целый PCM поддерживаются")
    if audio.channels <= 0 or audio.sample_rate <= 0:
        raise ValueError("Количество каналов и частота дискретизации должны быть положительными")
    if len(audio.samples) % audio.channels:
        raise ValueError("Неправильный формат аудио-фрейма: нечетное количество каналов")
    limit = 1 << (8 * audio.sample_width - 1)
    if any(not isinstance(sample, int) or not -limit <= sample < limit
           for sample in audio.samples):
        raise ValueError("Аудиоданные PCM вне объявленной битовой глубины")


def read_wav(path):
    try:
        with wave.open(str(path), "rb") as file:
            channels = file.getnchannels()
            sample_rate = file.getframerate()
            width = file.getsampwidth()
            frame_count = file.getnframes()
            if file.getcomptype() != "NONE" or width not in (1, 2, 3, 4):
                raise ValueError("Только не сжатый аудио в формате 8/16/24/32-бит PCM WAV поддерживается")
            raw = file.readframes(frame_count)
    except (wave.Error, EOFError) as error:
        raise ValueError(
            f"Не удалось прочитать аудио-файл в формате PCM WAV (сжатые/флоат-формат WAV не поддерживаются): {error}"
        ) from error

    if len(raw) != frame_count * channels * width:
        raise ValueError("WAV содержит усечённую аудиоданные")
    if width == 1:
        samples = [value - 128 for value in raw]
    else:
        samples = [
            int.from_bytes(raw[i:i + width], "little", signed=True)
            for i in range(0, len(raw), width)
        ]
    audio = AudioData(samples, channels, sample_rate, width)
    validate_audio(audio)
    return audio


def quantized_levels(audio):
    validate_audio(audio)
    bits = 8 * audio.sample_width
    offset = 1 << (bits - 1)
    return [(sample + offset) >> (bits - 8) for sample in audio.samples]


def audio_histogram(audio):
    return count_levels(quantized_levels(audio))


def quantize_audio(audio):
    levels = quantized_levels(audio)
    return AudioData(
        [level - 128 for level in levels],
        audio.channels, audio.sample_rate, 1,
    )


def write_wav(path, audio):
    validate_audio(audio)
    if audio.sample_width == 1:
        raw = bytes(sample + 128 for sample in audio.samples)
    else:
        raw = b"".join(
            sample.to_bytes(audio.sample_width, "little", signed=True)
            for sample in audio.samples
        )
    with wave.open(str(path), "wb") as file:
        file.setnchannels(audio.channels)
        file.setsampwidth(audio.sample_width)
        file.setframerate(audio.sample_rate)
        file.writeframes(raw)
