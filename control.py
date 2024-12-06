import cv2
import mediapipe as mp
import requests

# Khởi tạo MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,  # Chỉ nhận diện 1 bàn tay
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)

# Địa chỉ IP ESP32-CAM (thay bằng địa chỉ thực tế)
ESP32_CAM_URL = "http://192.168.4.2"

# Hàm gửi lệnh tới ESP32-CAM
def send_command(command):
    """Gửi lệnh điều khiển tới ESP32-CAM."""
    try:
        response = requests.get(f"{ESP32_CAM_URL}/action?go={command}")
        print(f"Sent command: {command}, Response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending command: {e}")

# Hàm xác định hành động dựa trên vị trí các ngón tay
def detect_hand_gesture(hand_landmarks):
    thumb_tip = hand_landmarks[4]
    index_tip = hand_landmarks[8]
    middle_tip = hand_landmarks[12]
    
    # Kiểm tra ngón trỏ chỉ lên, xuống, trái, phải
    if index_tip.y < middle_tip.y - 0.05:  # Ngón trỏ giơ lên (tiến)
        send_command("forward")
    elif index_tip.y > middle_tip.y + 0.05:  # Ngón trỏ chỉ xuống (lùi)
        send_command("backward")
    elif index_tip.x < thumb_tip.x - 0.05:  # Ngón trỏ chỉ trái
        send_command("right")
    elif index_tip.x > thumb_tip.x + 0.05:  # Ngón trỏ chỉ phải
        send_command("left")
    else: send_command("stop")

# Mở camera
cap = cv2.VideoCapture(0)

print("Start!........")



while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Không thể lấy dữ liệu từ camera.")
        break

    # Lật hình ảnh theo chiều ngang
    frame = cv2.flip(frame, 1)

    # Chuyển ảnh sang RGB để xử lý
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Phát hiện bàn tay
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Kiểm tra cử chỉ ngón tay
            detect_hand_gesture(hand_landmarks.landmark)


    # Hiển thị hình ảnh
    cv2.imshow('Hand Gesture Control', frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
