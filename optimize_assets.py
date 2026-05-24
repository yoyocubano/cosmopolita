import os
from PIL import Image, ImageSequence

assets_dir = "/Users/yoyocubano/Documents/ANTIGRAVITY_CORE_DO_NOT_DELETE/projects/cosmopolita/assets"
webp_files = [f for f in os.listdir(assets_dir) if f.endswith('.webp')]

TARGET_WIDTH = 400
FRAME_SKIP = 2  # Keep 1 out of every 2 frames
QUALITY = 40

for filename in webp_files:
    filepath = os.path.join(assets_dir, filename)
    print(f"Optimizing {filename}...")
    
    try:
        img = Image.open(filepath)
        
        frames = []
        durations = []
        
        # Read frames
        for i, frame in enumerate(ImageSequence.Iterator(img)):
            if i % FRAME_SKIP == 0:
                # Resize frame
                aspect = frame.height / frame.width
                new_h = int(TARGET_WIDTH * aspect)
                resized_frame = frame.resize((TARGET_WIDTH, new_h), Image.Resampling.LANCZOS)
                
                # Convert to RGB (WebP saves best from RGB/RGBA)
                frames.append(resized_frame.convert("RGB"))
                
                # Accumulate duration (if original had duration info)
                # Typically, webp duration is in info['duration']
                orig_dur = frame.info.get('duration', 83) # 83ms = ~12fps fallback
                durations.append(orig_dur * FRAME_SKIP)
        
        if frames:
            temp_filepath = filepath + ".tmp.webp"
            
            # Save optimized
            frames[0].save(
                temp_filepath,
                format='WebP',
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0,
                quality=QUALITY,
                method=6  # Max compression effort
            )
            
            # Replace original
            orig_size = os.path.getsize(filepath)
            new_size = os.path.getsize(temp_filepath)
            
            os.replace(temp_filepath, filepath)
            
            print(f"  Done: {orig_size / 1024 / 1024:.2f} MB -> {new_size / 1024 / 1024:.2f} MB (Saved {(1 - new_size/orig_size)*100:.1f}%)")
            
    except Exception as e:
        print(f"  Failed to process {filename}: {e}")

print("Optimization complete.")
