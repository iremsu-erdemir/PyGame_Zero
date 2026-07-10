# Forest Runner

## Game Type
Platformer / Runner

## How to Run
```bash
pgzrun game.py
```

If `pgzrun` is not on PATH on Windows:

```bash
python -m pgzero game.py
```

## Controls
- Left/A: Move left
- Right/D: Move right
- Up/Space: Jump
- Mouse: Use the menu buttons
- Enter: Return to menu from win/lose screens

## Game Mechanics
- Collect all 4 coins, then reach the flag to win.
- Hitting an enemy or falling off the level triggers a loss.
- Enemies patrol platforms and pause briefly at the edges.

## Used Modules
- `pygame` module: `Rect` only
- Pygame Zero runtime globals: `screen`, `images`, `sounds`, `music`, `keyboard`, `keys`

## Asset Credits
Görsel ve ses kaynakları proje klasöründeki yerel assetlerden alınmıştır.

- Player sprite seti Fat Berry character pack tabanlıdır.
- Player sprite'ları: `images/idle*.png`, `images/run*.png`, `images/jump*.png`
- Düşman sprite'ları: `images/enemy_idle_*.png`, `images/enemy_walk_*.png`
- Coin görseli: `images/coin.png`
- Bayrak/hedef görseli: `images/flag.png`
- Arka plan müziği: `music/background.mp3`
- Ses efektleri: `sounds/coin.wav`, `sounds/jump.wav`, `sounds/hit.wav`, `sounds/win.wav`
- Legacy unused player placeholders remain in `images/` for reference: `images/player_idle_0.png`, `images/player_idle_1.png`, `images/player_run_0.png`, `images/player_run_1.png`.

## Submission
- Share the repository link directly; do not submit a zip archive.
- Make sure the repo is public or accessible to the evaluator.
- Keep the top-level structure intact: `game.py`, `images/`, `music/`, `sounds/`, `README.md`.
- Run the game with `pgzrun game.py` or `python -m pgzero game.py`.