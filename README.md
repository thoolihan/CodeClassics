# CodeClassics

Python implementations of classic arcade games from the book [Code the Classics](https://wireframe.raspberrypi.com/books/code-the-classics1) (Raspberry Pi Press), built with [Pygame Zero](https://pygame-zero.readthedocs.io/).

## Games

| Chapter | Game | Description |
|---|---|---|
| [ch01-boing/](ch01-boing/) | **Boing** | Pong clone |
| [ch02-cavern/](ch02-cavern/) | **Cavern** | Platformer/arcade game |
| [ch03-bunner/](ch03-bunner/) | **Bunner** | Frogger-style game |

Reference implementations from the book are in [book/](book/).

## Setup

Game assets (images, music, sounds) are not duplicated in the repo. Copy them from the reference versions by running:

- **bash:** `./copy-images.bash`
- **Windows:** `copy-images.bat`

## Running

Dependencies are managed with [uv](https://docs.astral.sh/uv/). To run a game:

```bash
uv run pgzrun ch01-boing/boing.py
uv run pgzrun ch02-cavern/cavern.py
uv run pgzrun ch03-bunner/bunner.py
```

`uv run` will automatically install dependencies on first run.
