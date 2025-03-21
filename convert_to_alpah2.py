from PIL import Image
import os

input_dir = "frames_removed"
output_dir = "frames_padded"
os.makedirs(output_dir, exist_ok=True)

target_size = (1024, 1024)  # 원하는 고정 캔버스 사이즈

for filename in sorted(os.listdir(input_dir)):
    if filename.endswith(".png"):
        img = Image.open(os.path.join(input_dir, filename)).convert("RGBA")

        # 새 투명 배경 캔버스 생성
        new_img = Image.new("RGBA", target_size, (0, 0, 0, 0))

        # 기존 이미지 중앙에 붙이기
        offset = ((target_size[0] - img.width) // 2, (target_size[1] - img.height) // 2)
        new_img.paste(img, offset, mask=img)

        new_img.save(os.path.join(output_dir, filename))
