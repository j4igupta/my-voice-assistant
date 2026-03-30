import cv2
import os


def capture_image(output_path: str = "frame.jpg") -> str | None:
    """Capture a single frame from the default camera and save it as JPEG.
    
    Returns the file path on success, or None on failure.
    Resizes to 640x480 before saving — significantly reduces Gemini latency.
    """
    cap = cv2.VideoCapture(0)  # 0 = default/first camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    # Let camera auto-adjust for a couple frames before capturing
    for _ in range(3):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        print("Error: Failed to capture frame.")
        return None

    # Resize for faster upload / lower latency with Gemini
    frame = cv2.resize(frame, (640, 480))

    cv2.imwrite(output_path, frame)
    print(f"Image captured: {output_path}")
    return output_path
