import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Multi QR Decoder",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Đọc nhiều QR Code trong 1 ảnh")

st.write("Kéo thả ảnh vào, hệ thống sẽ tự động đọc tất cả QR trong ảnh.")

uploaded_file = st.file_uploader(
    "Chọn ảnh",
    type=["jpg", "jpeg", "png"]
)

def decode_qr(image):
    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, _ = detector.detectAndDecodeMulti(image)

    if retval:
        return [text for text in decoded_info if text]
    return []

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    st.image(image, caption="Ảnh đã upload", use_container_width=True)

    results = decode_qr(img_np)

    if results:
        st.success(f"✅ Phát hiện {len(results)} QR:")
        for i, r in enumerate(results, 1):
            st.write(f"**{i}.** {r}")
    else:
        st.warning("❌ Không phát hiện QR nào trong ảnh")
