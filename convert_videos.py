import cv2
from PIL import Image
import os
import glob

def process_video(video_path, output_path, target_width=600, fps=12):
    print(f"Processing {video_path}...")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open {video_path}")
        return

    frames = []
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    if original_fps == 0 or original_fps != original_fps:
        original_fps = 24
        
    frame_skip = max(1, int(original_fps / fps))
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if count % frame_skip == 0:
            h, w = frame.shape[:2]
            
            # Calculate resize
            aspect = h / w
            new_w = target_width
            new_h = int(new_w * aspect)
            frame = cv2.resize(frame, (new_w, new_h))
            
            # Blur bottom right watermark (veo)
            # Estimate watermark size: 15% width, 10% height
            wm_w = int(new_w * 0.20)
            wm_h = int(new_h * 0.12)
            roi = frame[new_h - wm_h:new_h, new_w - wm_w:new_w]
            blurred_roi = cv2.GaussianBlur(roi, (51, 51), 30)
            frame[new_h - wm_h:new_h, new_w - wm_w:new_w] = blurred_roi
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)
            frames.append(pil_img)
            
        count += 1
        
    cap.release()
    
    if frames:
        print(f"Saving {len(frames)} frames to {output_path}...")
        frames[0].save(
            output_path,
            format='WebP',
            save_all=True,
            append_images=frames[1:],
            duration=int(1000/fps),
            loop=0,
            quality=80
        )
        print(f"Saved {output_path}")

video_dir = os.path.expanduser("~/Desktop/All_Projects_Assets/cosmopolita/VIDEOS /")
output_dir = "/Users/yoyocubano/Documents/ANTIGRAVITY_CORE_DO_NOT_DELETE/projects/cosmopolita/assets"

tasks = [
    ("ARROZ_CON_COCO_blueprint_recipe_202605172127.mp4", "arroz_con_coco.webp"),
    ("Arroz_a_la_Valenciana_blueprint_202605172132.mp4", "arroz_a_la_valenciana.webp"),
    ("PABELLON .mp4", "pabellon.webp"),
    ("ROPA VIEJA .mp4", "ropa_vieja.webp")
]

for src_name, dest_name in tasks:
    src_path = os.path.join(video_dir, src_name)
    dest_path = os.path.join(output_dir, dest_name)
    if os.path.exists(src_path):
        process_video(src_path, dest_path)

# Handle the glob for congri
congri_files = glob.glob(os.path.join(video_dir, "Cuban_Arroz*2117.mp4"))
if congri_files:
    process_video(congri_files[0], os.path.join(output_dir, "arroz_con_gris.webp"))
