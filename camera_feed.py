from picamera2 import Picamera2
import cv2
import numpy as np


class CameraFeed:
    def __init__(self):
        # Initialize the Picamera2
        self.picam2 = Picamera2()
        self.height = 480
        self.width = 480

        # Configure camera settings
        self.config = self.picam2.create_video_configuration(
            main={"format": 'XRGB8888', "size": (self.height, self.width)},
            controls={
                "FrameDurationLimits": (8333, 8333),
                "ExposureTime": 8000
            }
        )
        self.picam2.configure(self.config)

        # Define HSV range for fluorescent pink
        self.lower_pink = np.array([125, 100, 100])
        self.upper_pink = np.array([155, 255, 255])

        # Start the camera
        self.picam2.start()

    def take_pic(self):
        # Capture image in RGB format and convert to BGR for OpenCV
        image_rgb = self.picam2.capture_array()
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        return image_bgr

    def show_video(self, image):
        # Display the image
        cv2.imshow("Live Feed", image)
        cv2.waitKey(1)

    def find_ball(self, image):
        # Convert image to HSV color space
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Create a mask for the pink color
        mask = cv2.inRange(image_hsv, self.lower_pink, self.upper_pink)
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(largest_contour)
            area = cv2.contourArea(largest_contour)

            if area > 200:  # Threshold to ignore small areas (noise)
                # Draw a circle around the detected pink object
                cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                self.show_video(image)
                d = radius * 2
                h = 10000 / d  # Some hypothetical height calculation
                # Adjust coordinates
                x -= self.height / 2
                y -= self.width / 2
                x, y = -y, x
                return int(x), int(y), int(area)  # Return coordinates and area of the detected object

        # Show video if no ball is found
        self.show_video(image)
        return -1, -1, 0  # Return -1, -1 if no pink object is detected

    def close_cam(self):
        # Stop the camera and close OpenCV windows
        self.picam2.stop()
        self.picam2.close()
        cv2.destroyAllWindows()


