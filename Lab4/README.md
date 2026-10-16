# Lab 4: VibeCoding

**Assigned repo:** [SETAPESU26/41_fruit-ninja](https://github.com/SETAPESU26/41_fruit-ninja)  
**Author:** Akshansh Agrawal (PES2UG24CS045)

A Pygame Fruit Ninja-style game was fixed and extended by prompting an AI coding assistant.

## Deliverables

| Deliverable | Location | Contents |
| --- | --- | --- |
| Videos | [Before_fix_Fruit_Ninja.mp4](Videos/Before_fix_Fruit_Ninja.mp4), [After_fix_Fruit_Ninja.mp4](Videos/After_fix_Fruit_Ninja.mp4) | Gameplay clips from before and after the changes |
| Updated Code | [Code/](Code/) | The fixed game with all four README tasks done |
| Chat History | [Chat_History/](Chat_History/) | The full AI chat, exported as a PDF |

## Changes

| Task | What changed | Files |
| --- | --- | --- |
| 1. Collision detection | Fast swipes used to skip over fruit because only single mouse points were checked. Now the whole blade segment between two mouse positions is tested against each fruit's circle. After playtesting, fruit that flew into the still-visible blade trail also weren't being cut, so every frame now checks the whole visible trail against each fruit's new position. | `game/fruit.py`, `game/game_engine.py` |
| 2. Game Over screen | The console print is replaced with an overlay that shows the reason, the final score and the session best. The blade no longer slices or scores after the game ends, and lives never go below 0. | `game/game_engine.py` |
| 3. Replay option | On the Game Over screen, choose Easy, Medium or Hard (keys 1/2/3 or click) to play again with a different spawn rate, bomb chance and launch speed, or press Q / Esc to quit. | `game/game_engine.py`, `main.py` |
| 4. Sound effects | A slice swish, a bomb explosion and a game-over jingle are generated in code, so no audio files are needed. If no audio device is found, the game runs silently. | `game/sounds.py`, `main.py` |

| Difficulty | Frames between spawns | Bomb chance | Launch speed |
| --- | --- | --- | --- |
| Easy | 70 | 8% | 0.95x |
| Medium | 55 | 15% | 1.0x |
| Hard | 38 | 25% | 1.1x |

## Running

`requirements.txt` uses `pygame-ce` because the original `pygame` package has no build for Python 3.14. It is a drop-in replacement, so the code still runs `import pygame`.

```bash
cd Lab4/Code
pip install -r requirements.txt
python main.py
```
