import os
import pandas as pd
import openai
from moviepy.editor import *
from pathlib import Path
from dotenv import load_dotenv
import time

# ✅ PNG 시퀀스 기반 아바타 오버레이
from moviepy.editor import ImageSequenceClip

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 경로 설정
SCRIPT_PATH = "script.xlsx"
SLIDE_PATH = Path("slides")
AUDIO_PATH = Path("audios")
AVATAR_FRAMES = "frames_padded"  # ✅ padded된 PNG 시퀀스 사용
OUTPUT_PATH = "with_avatar_animated.mp4"

AUDIO_PATH.mkdir(parents=True, exist_ok=True)


# OpenAI TTS 생성 함수
def generate_tts(text, filename):
    response = openai.audio.speech.create(model="tts-1", voice="fable", input=text)
    with open(filename, "wb") as f:
        f.write(response.content)


# 엑셀 스크립트 불러오기
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

# 슬라이드 영상 합치기
final_video = concatenate_videoclips(video_clips, method="compose")
final_audio = CompositeAudioClip(audio_clips)
final_video = final_video.set_audio(final_audio)

# ✅ padded된 PNG 시퀀스 기반 캐릭터 오버레이
avatar = (
    ImageSequenceClip(AVATAR_FRAMES, fps=30)
    .resize(height=300)
    .set_position(("right", "bottom"))
    .loop(duration=final_video.duration)
)

# 아바타와 영상 합성
composite = CompositeVideoClip([final_video, avatar])

# ⏱ 영상 렌더링 시작
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
