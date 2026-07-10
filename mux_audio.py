"""
Mux Blue Diamond soundtrack onto the LIKE ME IN 16K video.
Create multiple versions:
1. First 28.2s of track synced to video
2. Video looped to match full track duration (169.6s)
"""
import subprocess, os, json

AUDIO_PATH = r'C:\Users\emupa\Downloads\Blue Diamond.mp3'
VIDEO_PATH = r'C:\Users\emupa\like-me-16k\LIKE_ME_IN_16K_Part_II.mp4'
OUTPUT_DIR = r'C:\Users\emupa\like-me-16k'
AUDIO_DIR = os.path.join(OUTPUT_DIR, 'audio')
os.makedirs(AUDIO_DIR, exist_ok=True)

# Version 1: First 28.2s of track onto video
out1 = os.path.join(OUTPUT_DIR, 'LIKE_ME_IN_16K_Part_II_with_audio.mp4')
print('Version 1: Sync first 28.2s of Blue Diamond to video...')
cmd1 = [
    'ffmpeg', '-y',
    '-i', VIDEO_PATH,
    '-i', AUDIO_PATH,
    '-t', '28.2',
    '-map', '0:v:0', '-map', '1:a:0',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '192k',
    '-shortest',
    '-preset', 'medium',
    out1
]
r1 = subprocess.run(cmd1, capture_output=True, text=True, timeout=180)
if r1.returncode == 0:
    sz = os.path.getsize(out1)
    print(f'  OK: {sz:,} bytes ({sz/1024/1024:.1f} MB)')
else:
    print(f'  FAILED: {r1.stderr[-300:]}')

# Version 2: Use the most dramatic 30s segment (skip intro, start at ~30s where beat likely drops)
out2 = os.path.join(OUTPUT_DIR, 'LIKE_ME_IN_16K_Part_II_drop_mix.mp4')
print('Version 2: Drop segment (30s offset) synced to video...')
cmd2 = [
    'ffmpeg', '-y',
    '-i', VIDEO_PATH,
    '-ss', '30', '-t', '28.2',
    '-i', AUDIO_PATH,
    '-map', '0:v:0', '-map', '1:a:0',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '192k',
    '-shortest',
    '-preset', 'medium',
    out2
]
r2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=180)
if r2.returncode == 0:
    sz = os.path.getsize(out2)
    print(f'  OK: {sz:,} bytes ({sz/1024/1024:.1f} MB)')
else:
    print(f'  FAILED: {r2.stderr[-300:]}')

# Version 3: Loop video to full 169.6s track duration
out3 = os.path.join(OUTPUT_DIR, 'LIKE_ME_IN_16K_Part_II_FULL_TRACK.mp4')
print('Version 3: Loop video to full track (169.6s)...')

# Create a looped video using stream_loop
cmd3 = [
    'ffmpeg', '-y',
    '-stream_loop', '-1', '-i', VIDEO_PATH,
    '-i', AUDIO_PATH,
    '-map', '0:v:0', '-map', '1:a:0',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '192k',
    '-shortest',
    '-preset', 'medium',
    out3
]
r3 = subprocess.run(cmd3, capture_output=True, text=True, timeout=300)
if r3.returncode == 0:
    sz = os.path.getsize(out3)
    print(f'  OK: {sz:,} bytes ({sz/1024/1024:.1f} MB)')
else:
    print(f'  FAILED: {r3.stderr[-300:]}')

# Copy audio track separately for download
audio_copy = os.path.join(AUDIO_DIR, 'Blue_Diamond_soundtrack.mp3')
print('Copying audio track...')
import shutil
shutil.copy2(AUDIO_PATH, audio_copy)
print(f'  OK: {os.path.getsize(audio_copy):,} bytes')

# Print summary
print('\n=== All versions ===')
for name, path in [
    ('Short (first 28s)', out1),
    ('Drop mix (30s offset)', out2),
    ('Full track loop', out3),
]:
    if os.path.exists(path):
        # Get duration
        probe = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', path],
            capture_output=True, text=True, timeout=10
        )
        if probe.returncode == 0:
            info = json.loads(probe.stdout)
            dur = float(info.get('format', {}).get('duration', 0))
            sz = os.path.getsize(path)
            print(f'  {name}: {dur:.1f}s, {sz/1024/1024:.1f} MB')
