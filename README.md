# Forest Runner

## Game Name
Forest Runner

## Game Type
Platformer / Runner

## How to Run
```bash
pgzrun game.py
```

## Controls
- Sol Ok / A: Sola hareket
- Sağ Ok / D: Sağa hareket
- Yukarı Ok / Space: Zıpla
- Mouse: Menudeki butonlari kullan
- Enter: Win/Lose ekranindan menuye don

## Win Condition
Tüm coin'leri topladıktan sonra sondaki flag'e ulaşınca oyun kazanılır.

## Lose Condition
- Düşmanla çarpılırsanız
- Platformlardan düşüp ekranın altına inerseniz

## Used Modules
- `pygame` modülünden `Rect` ve `transform`
- Pygame Zero runtime özellikleri: `screen`, `images`, `sounds`, `music`, `keyboard`, `keys`

## Asset Credits
Görsel ve ses kaynakları proje klasöründeki yerel assetlerden alınmıştır.

- Player sprite'ları: `images/idle*.png`, `images/run*.png`, `images/jump*.png`
- Düşman sprite'ları: `images/enemy_idle_*.png`, `images/enemy_walk_*.png`
- Coin görseli: `images/coin.png`
- Bayrak/hedef görseli: `images/flag.png`
- Arka plan müziği: `music/background.mp3`
- Ses efektleri: `sounds/coin.wav`, `sounds/jump.wav`, `sounds/hit.wav`, `sounds/win.wav`

Not: Player sprite seti kod içindeki yorumda belirtildiği gibi Fat Berry character pack üzerine kuruludur.