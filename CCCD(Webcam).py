import cv2
import numpy as np
import pytesseract
import re
from collections import deque, Counter
import tkinter as tk
from tkinter import messagebox

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def execute_script():
    cap = cv2.VideoCapture(0)
    last_10_cmnd = deque(maxlen=10)

    while True:
        ret, image = cap.read()
        if image is not None:
            h, w = image.shape[:2]
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
            gray_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            cmnd_number = pytesseract.image_to_string(gray_image,
            config="--oem 1 --psm 3 tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ")
            matches = re.findall(r'\d{12,}', cmnd_number)
            if matches:
                last_match = matches[-1]
                cmnd_number = last_match[-12:] if len(last_match) > 12 else last_match
                last_10_cmnd.append(cmnd_number)
            else:
                cmnd_number = "Không tìm thấy số căn cước công dân"

            if len(last_10_cmnd) == 10:
                counter = Counter(last_10_cmnd)
                most_common_cmnd, _ = counter.most_common(1)[0]
                messagebox.showinfo("Số CMND", f"Số CMND : {most_common_cmnd}")
                break

            h, w = gray_image.shape
            boxes = pytesseract.image_to_boxes(gray_image)
            for b in boxes.splitlines():
                b = b.split(' ')
                img = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
            cv2.imshow('Webcam', image)
        else:
            print("Không thể đọc ảnh từ webcam!")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Create main window
root = tk.Tk()
root.title("Execute Script")

# Create execute button
execute_button = tk.Button(root, text="Execute Script", command=execute_script)
execute_button.pack(pady=10)

# Run the main loop
root.mainloop()
