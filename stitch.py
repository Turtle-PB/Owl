import subprocess, os

CLIPS_DIR = r'C:\Users\emupa\like-me-16k\clips'
OUTPUT_DIR = r'C:\Users\emupa\like-me-16k'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# List available clips
clips = sorted([f for f in os.listdir(CLIPS_DIR) if f.endswith('.mp4')])
print(f'Available clips: {clips}')

# Create a concat file
concat_path = os.path.join(OUTPUT_DIR, 'concat_list.txt')
with open(concat_path, 'w') as f:
    for clip in clips:
        clip_path = os.path.join(CLIPS_DIR, clip).replace('\\', '/')
        f.write(f"file '{clip_path}'\n")

print(f'Concat file created: {concat_path}')

# Stitch with ffmpeg
output_path = os.path.join(OUTPUT_DIR, 'like_me_16k_partial.mp4')
cmd = [
    'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
    '-i', concat_path,
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-r', '16',
    '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2',
    '-preset', 'medium',
    output_path
]

print(f'Running ffmpeg...')
result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
if result.returncode == 0:
    size = os.path.getsize(output_path)
    print(f'Partial video created: {output_path} ({size:,} bytes)')
else:
    print(f'ffmpeg error: {result.stderr[-500:]}')
