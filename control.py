import cv2
import mediapipe as mp
import requests

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,  # Recognize only one hand
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)

# IP address ESP32-CAM (replace your ESP'sIP address)
ESP32_CAM_URL = "http://192.168.4.2"

# Send command to ESP32-CAM
def send_command(command):
    try:
        response = requests.get(f"{ESP32_CAM_URL}/action?go={command}")
        print(f"Sent command: {command}, Response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending command: {e}")

def detect_hand_gesture(hand_landmarks):
    thumb_tip = hand_landmarks[4]
    index_tip = hand_landmarks[8]
    middle_tip = hand_landmarks[12]
    
    if index_tip.y < middle_tip.y - 0.05:  # Index finger raised (forward).
        send_command("forward")
    elif index_tip.y > middle_tip.y + 0.05:  # Index finger pointing down (backward)
        send_command("backward")
    elif index_tip.x < thumb_tip.x - 0.05:  # Index fingger pointing left
        send_command("right")
    elif index_tip.x > thumb_tip.x + 0.05:  # Index finger pointing right
        send_command("left")
    else: send_command("stop")

# open camera
cap = cv2.VideoCapture(0)

print("Start!........")



while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive data from camera")
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Detect the hand
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # Check the gesture and send the command
            detect_hand_gesture(hand_landmarks.landmark)


    # Diplay image
    cv2.imshow('Hand Gesture Control', frame)

    # Press 'q' to exit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
