import os
import pandas as pd
import openai
from moviepy.editor import *
from pathlib import Path
from dotenv import load_dotenv
import time

# .env 로드
load_dotenv()

# OpenAI API 키 불러오기
openai.api_key = os.getenv("OPENAI_API_KEY")

# 경로 설정
SCRIPT_PATH = "script.xlsx"
SLIDE_PATH = Path("slides")
AUDIO_PATH = Path("audios")
OUTPUT_PATH = "output.mp4"

# 오디오 디렉터리 생성
AUDIO_PATH.mkdir(parents=True, exist_ok=True)


# OpenAI TTS 함수
def generate_tts(text, filename):
    response = openai.audio.speech.create(
        model="tts-1", voice="echo", input=text  # shimmer, nova, echo 중 선택 가능
    )
    with open(filename, "wb") as f:
        f.write(response.content)


# Excel 스크립트 로딩
df = pd.read_excel(SCRIPT_PATH)

# 슬라이드별 텍스트 그룹화
grouped = df.groupby("slide_number")

video_clips = []
audio_clips = []

start_time = 0  # 영상 전체 타임라인 기준

for slide_num, group in grouped:
    slide_img_path = SLIDE_PATH / f"슬라이드{slide_num}.png"
    audio_filename = AUDIO_PATH / f"슬라이드{slide_num}.mp3"

    if not slide_img_path.exists():
        raise FileNotFoundError(f"{slide_img_path} not found")

    # 텍스트 합치기
    combined_text = " ".join(group["text"].tolist())

    # OpenAI TTS로 mp3 생성
    generate_tts(combined_text, audio_filename)

    # 음성 파일 로드
    audio_clip = AudioFileClip(str(audio_filename))
    duration = audio_clip.duration

    # 이미지 클립 생성 (오디오 길이만큼 지속)
    image_clip = (
        ImageClip(str(slide_img_path)).resize((1920, 1080)).set_duration(duration)
    )
    video_clips.append(image_clip)

    # 오디오 클립 시작 위치 지정
    audio_clip = audio_clip.set_start(start_time)
    audio_clips.append(audio_clip)

    # 다음 슬라이드의 시작 시간 계산
    start_time += duration

# 영상 + 오디오 합치기
final_video = concatenate_videoclips(video_clips, method="compose")
final_audio = CompositeAudioClip(audio_clips)
final_video = final_video.set_audio(final_audio)

# ⏱️ 영상 생성 시간 측정 시작
build_start = time.time()

# 출력
final_video.write_videofile(OUTPUT_PATH, fps=24)

# ⏱️ 종료 후 시간 출력
build_end = time.time()
elapsed = build_end - build_start
print(f"\n✅ 영상 생성 완료! 소요 시간: {elapsed:.2f}초")
