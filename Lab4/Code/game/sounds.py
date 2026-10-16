import array
import math
import random
import pygame

# Sound effects are synthesised at start-up so the game needs no audio
# files. If no audio device is available the game simply runs silently.

class SoundBank:
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(44100, -16, 1, 512)
            freq, size, channels = pygame.mixer.get_init()
            if size != -16:
                return  # only signed 16-bit buffers are generated below
            self.freq = freq
            self.channels = channels
            self.sounds = {
                "slice": self._make(self._slice_samples(), volume=0.5),
                "bomb": self._make(self._bomb_samples(), volume=0.8),
                "game_over": self._make(self._game_over_samples(), volume=0.5),
            }
            self.enabled = True
        except (pygame.error, TypeError):
            self.sounds = {}

    def play(self, name):
        if self.enabled:
            self.sounds[name].play()

    def _make(self, samples, volume):
        peak = max(abs(s) for s in samples) or 1.0
        scale = 32767 * volume / peak
        data = array.array("h")
        for s in samples:
            value = int(s * scale)
            for _ in range(self.channels):
                data.append(value)
        return pygame.mixer.Sound(buffer=data.tobytes())

    def _slice_samples(self):
        # Short "swish": a falling pitch sweep mixed with a little noise.
        duration = 0.13
        n = int(self.freq * duration)
        samples = []
        phase = 0.0
        for i in range(n):
            t = i / n
            pitch = 1400 - 1000 * t
            phase += 2 * math.pi * pitch / self.freq
            envelope = (1 - t) ** 2
            samples.append(envelope * (0.7 * math.sin(phase) + 0.3 * random.uniform(-1, 1)))
        return samples

    def _bomb_samples(self):
        # Explosion: low-pass filtered noise plus a low thump, decaying.
        duration = 0.7
        n = int(self.freq * duration)
        samples = []
        filtered = 0.0
        for i in range(n):
            t = i / self.freq
            filtered += 0.08 * (random.uniform(-1, 1) - filtered)
            thump = math.sin(2 * math.pi * 55 * t)
            envelope = math.exp(-6 * t)
            samples.append(envelope * (filtered * 4 + 0.6 * thump))
        return samples

    def _game_over_samples(self):
        # Three descending notes (G4, Eb4, C4).
        notes = [(392.0, 0.2), (311.1, 0.2), (261.6, 0.5)]
        samples = []
        for pitch, duration in notes:
            n = int(self.freq * duration)
            for i in range(n):
                t = i / self.freq
                attack = min(1.0, t / 0.01)
                envelope = attack * math.exp(-3 * t)
                wave = math.sin(2 * math.pi * pitch * t) + 0.3 * math.sin(2 * math.pi * pitch * 3 * t)
                samples.append(envelope * wave)
        return samples
