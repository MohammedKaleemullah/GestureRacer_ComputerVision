import cv2
import Gesture_Racer 
def main():
    cap = cv2.VideoCapture(0)
    tracker = Gesture_Racer.HandTracker()
    while True:
        success, image = cap.read()
        image = cv2.flip(image, 1)
        image = tracker.hands_finder(image)
        cv2.imshow("Video", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()