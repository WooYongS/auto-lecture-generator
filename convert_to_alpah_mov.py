import os
from pathlib import Path
from rembg import remove
from PIL import Image
import subprocess

# 설정
input_video = "avatar.mov"  # 원본 영상 (배경 있음)
frame_rate = 30  # FPS
frame_dir = Path("frames")
removed_dir = Path("frames_removed")
output_mov = "avatar_clean.mov"


# 1️⃣ 프레임 추출
def extract_frames():
    frame_dir.mkdir(exist_ok=True)
    cmd = ["ffmpeg", "-y", "-i", input_video, str(frame_dir / "frame_%04d.png")]
    subprocess.run(cmd, check=True)
    print("✅ Step 1: 프레임 추출 완료")


# 2️⃣ rembg로 배경 제거
def remove_background():
    removed_dir.mkdir(exist_ok=True)
    for file in sorted(frame_dir.glob("frame_*.png")):
        with Image.open(file).convert("RGBA") as img:
            output = remove(img)
            output.save(removed_dir / file.name)
    print("✅ Step 2: 배경 제거 완료")


# 3️⃣ MOV(ProRes 4444)로 재조합
def generate_mov():
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(frame_rate),
        "-i",
        str(removed_dir / "frame_%04d.png"),
        "-c:v",
        "prores_ks",
        "-profile:v",
        "4444",
        "-pix_fmt",
        "yuva444p10le",
        output_mov,
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ Step 3: MOV 생성 완료 → {output_mov}")


# 전체 파이프라인 실행
if __name__ == "__main__":
    extract_frames()
    remove_background()
    generate_mov()
