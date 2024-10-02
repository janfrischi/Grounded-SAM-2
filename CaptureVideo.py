import os
import cv2
import pyzed.sl as sl


# Initialize the ZED camera
def initialize_zed():
    zed = sl.Camera()

    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720  # Set resolution
    init_params.depth_mode = sl.DEPTH_MODE.NONE  # We don't need depth data for this task

    if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
        print("Error: Unable to open ZED camera")
        exit()

    return zed


# Create a directory for saving captured images
def create_output_directory(base_dir="custom_video_frames"):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return base_dir


# Capture images from the ZED camera and save them when recording is active
def capture_images(zed, save_directory):
    image = sl.Mat()
    frame_count = 0
    recording = False

    print("Press 'Space' to start/stop recording. Press 'q' to quit.")

    while True:
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.LEFT)  # Capture the left image from the stereo camera
            image_np = image.get_data()  # Convert to numpy array

            # Display the live feed
            cv2.imshow('Live ZED Camera Feed', image_np)

            # If recording is active, save the frame with zero-padded filename
            if recording:
                frame_filename = os.path.join(save_directory, f"{frame_count:05d}.jpg")  # Zero-padded filename
                cv2.imwrite(frame_filename, image_np)
                print(f"Saved: {frame_filename}")
                frame_count += 1

            # Handle key presses
            key = cv2.waitKey(1) & 0xFF

            if key == ord(' '):  # Space bar pressed to toggle recording
                recording = not recording
                if recording:
                    print("Recording started...")
                else:
                    print("Recording stopped.")

            elif key == ord('q'):  # Quit the program
                print("Exiting...")
                break

    # Close the camera and OpenCV windows
    zed.close()
    cv2.destroyAllWindows()


def main():
    # Initialize the ZED camera
    zed = initialize_zed()

    # Create a directory for storing captured images
    save_directory = create_output_directory("custom_video_frames")

    # Start capturing images (recording controlled by space bar)
    capture_images(zed, save_directory)


if __name__ == "__main__":
    main()
