```

python3.11 --version

python3.11 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install ipykernel


## 설치된 라이브러리 리스트 정리
pip freeze > requirements.txt

```

```
Sora로 mp4 영상 생성 후 mov로 전환
배경 투명색 아닐 경우 PNG시퀀스로 돌리고 다시 mov로 전환

* PNG 시퀀스를 MOV로 다시 합치기 (투명 배경 유지)
ffmpeg -framerate 30 -i frames_removed/frame_%04d.png \
-c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le avatar_clean.mov


ffmpeg로 PNG 시퀀스 → avatar_clean.mov로 변환 (완료)
```

ppt-lecture-agent/
├── venv/ # 가상환경
├── notebooks/ # Jupyter 노트북 모음
│ └── 01_slide_to_video.ipynb
├── scripts/ # python 파일로 로직화 시 보관
├── output/ # 영상/오디오 결과물
├── slides/ # PPT 파일 저장
├── requirements.txt
└── README.md

✅ OpenAI TTS의 기본 제공 음성 (2024년 기준)
음성 이름 성별/톤 특징
shimmer 여성, 밝고 선명 💁 가장 자연스럽고 일반적인 느낌
nova 여성, 중성 톤 🎓 설명형, 강의톤에 적합
echo 남성, 부드럽고 젊은 👦 부드러운 남성 목소리
onyx 남성, 차분하고 성숙 👨 낮고 안정적인 발표톤
fable 여성, 이야기하는 느낌 📚 동화/설명 스타일
alloy 남성, 캐주얼/라디오톤 🎙️ 경쾌하고 현대적인 느낌
