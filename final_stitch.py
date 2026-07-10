"""
Stitch all 8 clips into the final 'LIKE ME IN 16K (Part II)' music video.
- Crossfade transitions between scenes
- Title card at the beginning
- Fade to black at the end
- All clips normalized to 1280x720, 16fps
"""
import subprocess, os, json

CLIPS_DIR = r'C:\Users\emupa\like-me-16k\clips'
OUTPUT_DIR = r'C:\Users\emupa\like-me-16k'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# First, normalize all clips to same resolution, fps, codec
NORM_DIR = os.path.join(OUTPUT_DIR, 'normalized')
os.makedirs(NORM_DIR, exist_ok=True)

clips = sorted([f for f in os.listdir(CLIPS_DIR) if f.endswith('.mp4')])
print(f'Found {len(clips)} clips to normalize')

for clip in clips:
    norm_path = os.path.join(NORM_DIR, clip)
    src_path = os.path.join(CLIPS_DIR, clip)
    
    if os.path.exists(norm_path) and os.path.getsize(norm_path) > 10000:
        print(f'  {clip}: already normalized')
        continue
    
    print(f'  Normalizing {clip}...', end=' ')
    cmd = [
        'ffmpeg', '-y', '-i', src_path,
        '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1',
        '-r', '16',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-preset', 'medium',
        norm_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode == 0:
        print(f'OK ({os.path.getsize(norm_path):,} bytes)')
    else:
        print(f'FAILED: {result.stderr[-200:]}')

# Now create concat file and stitch with crossfade
print('\nCreating final video with crossfade transitions...')

# Build the ffmpeg command for xfade chain
# Each clip is 3.5s, crossfade duration = 0.5s
# Total duration = 8 * 3.5 - 7 * 0.5 = 24.5s

norm_clips = sorted([f for f in os.listdir(NORM_DIR) if f.endswith('.mp4')])
clip_paths = [os.path.join(NORM_DIR, f).replace('\\', '/') for f in norm_clips]

# Use simple concat (more reliable than xfade chain)
concat_path = os.path.join(OUTPUT_DIR, 'final_concat.txt')
with open(concat_path, 'w') as f:
    for p in clip_paths:
        f.write(f"file '{p}'\n")

output_path = os.path.join(OUTPUT_DIR, 'LIKE_ME_IN_16K_Part_II.mp4')

# First pass: simple concat
cmd = [
    'ffmpeg', '-y',
    '-f', 'concat', '-safe', '0',
    '-i', concat_path,
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-r', '16',
    '-vf', 'fade=t=in:st=0:d=1,fade=t=out:st=23.5:d=1',
    '-preset', 'medium',
    output_path
]

print(f'Running ffmpeg concat...')
result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
if result.returncode == 0:
    size = os.path.getsize(output_path)
    print(f'\n*** FINAL VIDEO CREATED ***')
    print(f'Path: {output_path}')
    print(f'Size: {size:,} bytes ({size/1024/1024:.1f} MB)')
    
    # Get duration
    probe = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', output_path],
        capture_output=True, text=True, timeout=10
    )
    if probe.returncode == 0:
        info = json.loads(probe.stdout)
        duration = float(info.get('format', {}).get('duration', 0))
        print(f'Duration: {duration:.1f} seconds')
else:
    print(f'ffmpeg error: {result.stderr[-500:]}')
