from camera_feed import CameraFeed  # Save the above code as camera_feed.py and import it here
import time

# Initialize the camera feed
camera_feed = CameraFeed()

try:
    while True:
        # Capture an image
        image = camera_feed.take_pic()
        # Detect and mark the fluorescent pink object
        x, y, area = camera_feed.find_ball(image)
        print(f"Coordinates: ({x}, {y}), Area: {area}")
        time.sleep(0.1)  # Adjust the delay as needed

except KeyboardInterrupt:
    print("Stopping camera feed...")
    camera_feed.close_cam()

    

