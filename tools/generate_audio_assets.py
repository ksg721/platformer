"""Generate the small original audio set used by Vertical Ascent."""

import math
import struct
import wave
from pathlib import Path


SAMPLE_RATE = 44100
OUTPUT_DIRECTORY = Path(__file__).resolve().parents[1] / "assets" / "audio"


def write_wave(filename, samples):
    """Write floating-point samples as a mono 16-bit PCM WAV file."""
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIRECTORY / filename
    packed_samples = bytearray()
    for sample in samples:
        limited = max(-1.0, min(1.0, sample))
        packed_samples.extend(struct.pack("<h", int(limited * 32767)))

    with wave.open(str(output_path), "wb") as audio_file:
        audio_file.setnchannels(1)
        audio_file.setsampwidth(2)
        audio_file.setframerate(SAMPLE_RATE)
        audio_file.writeframes(packed_samples)


def envelope(index, total, attack=0.02, release=0.08):
    """Return a gentle attack/release envelope."""
    time = index / SAMPLE_RATE
    duration = total / SAMPLE_RATE
    attack_amount = min(1.0, time / max(attack, 0.001))
    release_amount = min(1.0, (duration - time) / max(release, 0.001))
    return max(0.0, min(1.0, attack_amount, release_amount))


def note(frequency, duration, volume=0.2, harmonics=(), tremolo=0.0):
    """Create one softly shaped note with optional harmonics."""
    total = max(1, int(duration * SAMPLE_RATE))
    samples = []
    for index in range(total):
        time = index / SAMPLE_RATE
        value = math.sin(2 * math.pi * frequency * time)
        for multiple, strength in harmonics:
            value += strength * math.sin(2 * math.pi * frequency * multiple * time)
        if tremolo:
            value *= 1.0 + tremolo * math.sin(2 * math.pi * 4.0 * time)
        samples.append(value * volume * envelope(index, total))
    return samples


def silence(duration):
    """Create silence for a musical rest."""
    return [0.0] * max(1, int(duration * SAMPLE_RATE))


def mix_tracks(tracks):
    """Mix equal-length or differing-length sample tracks together."""
    length = max(len(track) for track in tracks)
    mixed = [0.0] * length
    for track in tracks:
        for index, sample in enumerate(track):
            mixed[index] += sample
    scale = max(1.0, max(abs(sample) for sample in mixed) / 0.9)
    return [sample / scale for sample in mixed]


def make_menu_theme():
    """Create a calm, repeating menu progression."""
    progression = [(196.0, 2.0), (233.08, 2.0), (261.63, 2.0), (174.61, 2.0)]
    bass = sum(
        (note(frequency, duration, 0.11, ((2, 0.18),), 0.16)
         for frequency, duration in progression),
        [],
    )
    melody = []
    for frequency in (392.0, 349.23, 311.13, 349.23):
        melody.extend(note(frequency, 0.5, 0.06, ((2, 0.1),)))
        melody.extend(silence(1.5))
    return mix_tracks([bass, melody])


def make_climb_theme():
    """Create a gentle upward arpeggio for the main climb."""
    bass_notes = (146.83, 174.61, 196.0, 220.0, 196.0, 174.61)
    bass = sum(
        (note(frequency, 1.5, 0.10, ((2, 0.15),), 0.12)
         for frequency in bass_notes),
        [],
    )
    melody = []
    for frequency in (293.66, 349.23, 392.0, 440.0, 392.0, 349.23):
        melody.extend(note(frequency, 0.5, 0.07, ((2, 0.08),)))
        melody.extend(silence(1.0))
    return mix_tracks([bass, melody])


def make_fanfare():
    """Create a short summit fanfare."""
    return sum(
        (note(frequency, 0.42, 0.16, ((2, 0.12), (3, 0.06)))
         + silence(0.04) for frequency in (261.63, 329.63, 392.0, 523.25)),
        [],
    )


def make_land():
    """Create a soft low landing thump."""
    duration = 0.18
    total = int(duration * SAMPLE_RATE)
    samples = []
    for index in range(total):
        time = index / SAMPLE_RATE
        tone = math.sin(2 * math.pi * 105 * time)
        noise = math.sin(2 * math.pi * 37 * time) * 0.35
        samples.append((tone + noise) * 0.18 * math.exp(-18 * time))
    return samples


def make_wall_hit():
    """Create a short muted impact click."""
    duration = 0.12
    total = int(duration * SAMPLE_RATE)
    samples = []
    for index in range(total):
        time = index / SAMPLE_RATE
        tone = math.sin(2 * math.pi * 180 * time)
        samples.append(tone * 0.14 * math.exp(-28 * time))
    return samples


def make_menu_click():
    """Create a tiny interface confirmation sound."""
    return note(660.0, 0.08, 0.12, ((2, 0.08),))


def main():
    """Generate every audio asset used by the game."""
    write_wave("menu_theme.wav", make_menu_theme())
    write_wave("climb_theme.wav", make_climb_theme())
    write_wave("summit_fanfare.wav", make_fanfare())
    write_wave("land.wav", make_land())
    write_wave("wall_hit.wav", make_wall_hit())
    write_wave("menu_click.wav", make_menu_click())


if __name__ == "__main__":
    main()
