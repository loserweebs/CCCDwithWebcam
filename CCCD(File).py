import re

import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Đọc ảnh từ tệp
image_path = "cccd1.jpg"
image = cv2.imread(image_path)

# Kiểm tra xem ảnh đã được đọc thành công chưa
if image is not None:
    # Tăng độ phân giải
    h, w = image.shape[:2]
    image = cv2.resize(image, (2 * w, 2 * h), interpolation=cv2.INTER_LINEAR)

    # Chuyển ảnh sang độ xám
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Làm mờ ảnh
    gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Thay đổi ngưỡng
    _, gray_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # lưu ảnh(test)
    cv2.imwrite('result.jpg', gray_image)

    # Sử dụng thư viện pytesseract để nhận dạng số CMND
    cmnd_number = pytesseract.image_to_string(gray_image, config="--oem 1 --psm 6 tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ")
    # print("Thông tin CMND:", cmnd_number)

    # Tìm kiếm số căn cước công dân bằng regex
    # Tìm tất cả các chuỗi con chứa các chữ số
    matches = re.findall(r'\d{12,}', cmnd_number)

    # Nếu tìm thấy ít nhất một chuỗi con
    if matches:
        # Lấy chuỗi con cuối cùng (chứa các chữ số cuối cùng trong cmnd_number)
        last_match = matches[-1]

        # Nếu chuỗi con cuối cùng có nhiều hơn 12 chữ số
        if len(last_match) > 12:
            # Lấy 12 chữ số cuối cùng
            cmnd_number = last_match[-12:]
        else:
            # Nếu chuỗi con cuối cùng có đúng 12 chữ số
            cmnd_number = last_match
    else:
        cmnd_number = "Không tìm thấy số căn cước công dân"

    # Hiển thị số CMND
    print("Số CMND:", cmnd_number)
else:
    print("Không thể đọc ảnh từ tệp!")
