# 🎬 LIKE ME IN 16K (Part II) — Music Video

**Smooth Drill / Trap • Neon Digital • Emotional Futurism**

© 2024-2026 Paul Adcock / OwlLogics. All rights reserved. Patent rights reserved (35 U.S.C. 287a). MIT license applies to copyright only. Legal counsel on all IP.

## Final Video

**[`LIKE_ME_IN_16K_Part_II.mp4`](LIKE_ME_IN_16K_Part_II.mp4)** — 28.2 seconds, 1280x720, H264

## Concept

A neon-drenched music video exploring digital disconnection — two people lost between screens and reality. Cold blues, purple neon, warm golds. Russian and Spanish whispers woven through smooth drill energy.

## Scenes

| # | Title | Description | Animation |
|---|-------|-------------|-----------|
| 1 | Crystal Dreams | Neon apartment, phone glow, endless scrolling | Wan2.2 AI-animated |
| 2 | Corporate Toys / Digital Maze | Helmets, gadgets, ghost-like partner | Wan2.2 AI-animated |
| 3 | Frozen Connection | Slow-mo reach, glitch flicker | Wan2.2 AI-animated |
| 4 | Neon Bounce (Chorus) | Rooftop cityscape, drone orbit | Ken Burns zoom-in |
| 5 | Real World vs Screen World | Jeep, warm vs cold split | Ken Burns pan-right |
| 6 | Break the Interface | Holographic tunnel, swiping barriers | Ken Burns zoom-in |
| 7 | Return to Reality | Sunrise, gold tones, reunion | Ken Burns zoom-out |
| 8 | Stay With Me | Hands touching, cracked phone | Ken Burns zoom-in |

## Pipeline (100% Free, $0.00)

1. **Keyframe generation** — FLUX 2 Klein 9B via FAL.ai (8 cinematic stills)
2. **AI animation** — Wan2.2 I2V Lightning on Hugging Face Spaces (3 of 8 scenes animated before GPU quota exhausted)
3. **Fallback animation** — ffmpeg `zoompan` Ken Burns effect for remaining 5 scenes
4. **Assembly** — ffmpeg concat with fade in/out, normalized to 1280x720 @ 16fps

## File Structure

```
like-me-16k/
├── LIKE_ME_IN_16K_Part_II.mp4    # Final video
├── frames/                         # 8 keyframe PNG images (FLUX 2)
│   ├── scene_01.png ... scene_08.png
├── clips/                          # 8 individual video clips
│   ├── clip_01.mp4 ... clip_08.mp4
├── normalized/                     # Normalized 1280x720 versions
├── stitch.py                       # Basic concat script
├── ken_burns.py                    # Ken Burns effect generator
├── final_stitch.py                 # Final assembly with fades
└── event_ids.json                  # Gradio API event tracking
```

## Tools Used

- [FLUX 2 Klein 9B](https://fal.ai) — text-to-image
- [Wan2.2 I2V Lightning](https://huggingface.co/spaces/kulkas2pintu/wan555) — image-to-video (Hugging Face Space, free)
- [ffmpeg](https://ffmpeg.org/) — Ken Burns effects, normalization, final assembly

## License

© 2024-2026 Paul Adcock / OwlLogics. All rights reserved.
- Patent rights reserved under 35 U.S.C. 287a
- MIT license applies to copyright only
- Commercial use requires HMAC-SHA256 license key
- Legal counsel on all intellectual property
