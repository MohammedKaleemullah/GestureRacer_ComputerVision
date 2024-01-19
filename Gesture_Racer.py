import cv2
import mediapipe as mp
import keyboard
import Releaser

class HandTracker:
    
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, model_complexity=1, track_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.model_complexity = model_complexity
        self.track_confidence = track_confidence
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
        self.mode, self.max_hands, self.model_complexity,
        self.detection_confidence, self.track_confidence)
        self.mp_draw = mp.solutions.drawing_utils
        self.detected_gesture = None

    def hands_finder(self, image, draw=True):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image_rgb)
        num_hands=0
        if self.results.multi_hand_landmarks:
            num_hands = len(self.results.multi_hand_landmarks)
            y_diff_threshold = 35
            x_diff_threshold = 180
            top_hand_id = None
            top_hand_y = float('inf')
            top_hand_x = float('inf')
            for hand_id, hand_lms in enumerate(self.results.multi_hand_landmarks):
                hand_y = hand_lms.landmark[0].y * image.shape[0]
                hand_x = hand_lms.landmark[0].x * image.shape[0] 
                if hand_y < top_hand_y:
                    top_hand_id = hand_id
                    top_hand_y = hand_y
                if hand_x < top_hand_x:
                    top_hand_id = hand_id
                    top_hand_x = hand_x
            for hand_id, hand_lms in enumerate(self.results.multi_hand_landmarks):
                handedness = self.results.multi_handedness[hand_id]
                hand_label = "Right" if handedness.classification[0].label == "Right" else "Left"
                hand_y = hand_lms.landmark[0].y * image.shape[0] 
                hand_x = hand_lms.landmark[0].x * image.shape[0]
                if num_hands == 2:
                    if draw:
                        self.mp_draw.draw_landmarks(image, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                        if abs(hand_y - top_hand_y) > y_diff_threshold and hand_label == "Left":
                            cv2.putText(image, f"pressing Left", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            cv2.putText(image, f"releasing right", (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            keyboard.press('left')
                            keyboard.release('right')
                        elif abs(hand_y - top_hand_y) > y_diff_threshold and hand_label == "Right":
                            cv2.putText(image, f"pressing right", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            cv2.putText(image, f"releasing left", (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            keyboard.press('right')
                            keyboard.release('left')
                        elif  hand_id != top_hand_id and abs(hand_y - top_hand_y) < y_diff_threshold :
                            cv2.putText(image, f"Straight", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            keyboard.release('left')
                            keyboard.release('right')
                            cv2.putText(image, f"releasing l/r", (20, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        if abs(hand_x - top_hand_x)!=0 and num_hands == 2:
                            if abs(hand_x - top_hand_x)< x_diff_threshold:
                                keyboard.release('up')
                                cv2.putText(image,f"Releasing up",(20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            elif abs(hand_x - top_hand_x) > x_diff_threshold:
                                keyboard.press('up')
                                keyboard.release('down')
                                cv2.putText(image, f"Pressing up", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                cv2.putText(image, f"releasing down", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                else:
                    if draw:
                        self.mp_draw.draw_landmarks(image, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                        keyboard.release('up')
                        keyboard.release('left')
                        keyboard.release('right')
                        if num_hands==1:
                            keyboard.release('up')
                            keyboard.press('down')
                            cv2.putText(image, f"Releasing up", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            cv2.putText(image, f"Pressing down", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                            keyboard.release('up')
                            keyboard.release('down')
                            cv2.putText(image, f"Releasing down", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            cv2.putText(image, f"Releasing up", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if num_hands==0:
            Releaser.noHands(image)
        return image
    