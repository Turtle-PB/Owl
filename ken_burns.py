"""
Create Ken Burns effect videos for scenes 4-8 from the keyframe images.
Each image gets a slow zoom/pan effect to simulate camera motion.
"""
import subprocess, os

FRAMES_DIR = r'C:\Users\emupa\like-me-16k\frames'
CLIPS_DIR = r'C:\Users\emupa\like-me-16k\clips'
os.makedirs(CLIPS_DIR, exist_ok=True)

# Ken Burns effect configs for each scene
# (zoom_type: 'in' or 'out' or 'pan', direction for pan)
EFFECTS = {
    4: {'effect': 'in', 'desc': 'Slow zoom in on rooftop singer'},
    5: {'effect': 'pan_right', 'desc': 'Pan right across split perspective'},
    6: {'effect': 'in', 'desc': 'Slow zoom into tunnel'},
    7: {'effect': 'out', 'desc': 'Slow zoom out revealing sunrise'},
    8: {'effect': 'in', 'desc': 'Slow zoom in on hands touching'},
}

DURATION = 3.5  # seconds, matching the AI-generated clips
FPS = 16

for scene_num, config in EFFECTS.items():
    img_path = os.path.join(FRAMES_DIR, f'scene_{scene_num:02d}.png')
    clip_path = os.path.join(CLIPS_DIR, f'clip_{scene_num:02d}.mp4')
    
    if os.path.exists(clip_path) and os.path.getsize(clip_path) > 10000:
        print(f'Scene {scene_num}: already exists, skipping')
        continue
    
    print(f'Scene {scene_num}: {config["desc"]}...', end=' ')
    
    effect = config['effect']
    
    if effect == 'in':
        # Slow zoom in: scale from 1.0 to 1.15 over duration
        vf = (
            f"scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,"
            f"zoompan=z='min(zoom+0.0015,1.15)':d={int(DURATION*FPS)}:s=1280x720:fps={FPS}"
        )
    elif effect == 'out':
        # Slow zoom out: scale from 1.15 to 1.0
        vf = (
            f"scale=1472:828:force_original_aspect_ratio=decrease,pad=1472:828:(ow-iw)/2:(oh-ih)/2,"
            f"zoompan=z='max(zoom-0.0015,1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(DURATION*FPS)}:s=1280x720:fps={FPS}"
        )
    elif effect == 'pan_right':
        # Pan from left to right
        vf = (
            f"scale=1536:864:force_original_aspect_ratio=decrease,pad=1536:864:(ow-iw)/2:(oh-ih)/2,"
            f"zoompan=z=1.0:x='(iw-iw/1.2)*on/{int(DURATION*FPS)}':y='ih/2-(ih/zoom/2)':d={int(DURATION*FPS)}:s=1280x720:fps={FPS}"
        )
    
    cmd = [
        'ffmpeg', '-y',
        '-loop', '1', '-i', img_path,
        '-vf', vf,
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-t', str(DURATION),
        '-r', str(FPS),
        '-preset', 'medium',
        clip_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode == 0:
        size = os.path.getsize(clip_path)
        print(f'OK ({size:,} bytes)')
    else:
        print(f'FAILED: {result.stderr[-200:]}')

print('\n=== All Ken Burns clips created ===')
for f in sorted(os.listdir(CLIPS_DIR)):
    if f.endswith('.mp4'):
        p = os.path.join(CLIPS_DIR, f)
        print(f'{f}: {os.path.getsize(p):,} bytes')
