import os
import pandas as pd
import openai
from moviepy.editor import *
from pathlib import Path
from dotenv import load_dotenv
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

SCRIPT_PATH = "script.xlsx"
SLIDE_PATH = Path("slides")
AUDIO_PATH = Path("audios")
AVATAR_PATH = "avatar.png"  # 정지 이미지
OUTPUT_PATH = "with_avatar_still.mp4"

AUDIO_PATH.mkdir(parents=True, exist_ok=True)


def generate_tts(text, filename):
    response = openai.audio.speech.create(model="tts-1", voice="shimmer", input=text)
    with open(filename, "wb") as f:
        f.write(response.content)


df = pd.read_excel(SCRIPT_PATH)
grouped = df.groupby("slide_number")

video_clips = []
audio_clips = []
start_time = 0

for slide_num, group in grouped:
    slide_img_path = SLIDE_PATH / f"슬라이드{slide_num}.png"
    audio_filename = AUDIO_PATH / f"슬라이드{slide_num}.mp3"

    if not slide_img_path.exists():
        raise FileNotFoundError(f"{slide_img_path} not found")

    combined_text = " ".join(group["text"].tolist())
    generate_tts(combined_text, audio_filename)

    audio_clip = AudioFileClip(str(audio_filename))
    duration = audio_clip.duration

    image_clip = (
        ImageClip(str(slide_img_path)).resize((1920, 1080)).set_duration(duration)
    )
    video_clips.append(image_clip)

    audio_clip = audio_clip.set_start(start_time)
    audio_clips.append(audio_clip)

    start_time += duration

final_video = concatenate_videoclips(video_clips, method="compose")
final_audio = CompositeAudioClip(audio_clips)
final_video = final_video.set_audio(final_audio)

# ✅ 아바타 정지 이미지 오버레이
if not os.path.exists(AVATAR_PATH):
    raise FileNotFoundError(f"{AVATAR_PATH} not found")

avatar = (
    ImageClip(AVATAR_PATH)
    .resize(height=300)
    .set_position(("right", "bottom"))
    .set_duration(final_video.duration)
)


composite = CompositeVideoClip([final_video.set_opacity(1), avatar.set_opacity(1)])

start = time.time()
composite.write_videofile(
    OUTPUT_PATH,
    fps=24,
    codec="libx264",
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True,
)
elapsed = time.time() - start
print(f"\n✅ 영상 생성 완료! 소요 시간: {elapsed:.2f}초")
