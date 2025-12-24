import streamlit as st
import cv2
import numpy as np
from PIL import Image
from pyzbar.pyzbar import decode # Thư viện mạnh mẽ hơn cho pallet

st.set_page_config(page_title="Pallet QR Scanner", layout="wide")

st.title("📦 Hệ thống quét QR Pallet Hàng")

# 1. Chế độ lấy ảnh từ Camera
img_file_buffer = st.camera_input("Chụp ảnh pallet hàng")

def process_pallet(image_np):
    # Chuyển sang ảnh xám để tăng tốc độ nhận diện
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    
    # Giải mã bằng pyzbar
    barcodes = decode(gray)
    
    results = []
    for barcode in barcodes:
        # Lấy nội dung QR
        data = barcode.data.decode("utf-8")
        # Lấy vị trí khung hình chữ nhật
        (x, y, w, h) = barcode.rect
        # Vẽ khung xanh lên ảnh gốc
        cv2.rectangle(image_np, (x, y), (x + w, y + h), (0, 255, 0), 5)
        results.append(data)
        
    return image_np, results

if img_file_buffer:
    # Chuyển buffer thành ảnh numpy
    img = Image.open(img_file_buffer)
    img_np = np.array(img)

    # Xử lý
    processed_img, qr_list = process_pallet(img_np)

    # Hiển thị kết quả
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.image(processed_img, caption="Vị trí QR trên Pallet", use_container_width=True)

    with col2:
        st.subheader(f"📊 Tổng: {len(qr_list)} mã")
        if qr_list:
            # Loại bỏ trùng lặp nếu cần
            unique_qrs = list(set(qr_list))
            for i, code in enumerate(unique_qrs, 1):
                st.info(f"**{i}.** {code}")
        else:
            st.warning("Không tìm thấy mã nào. Hãy thử lại gần hơn.")