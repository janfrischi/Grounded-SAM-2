import pyzed.sl as sl
import cv2
import os


# Set up the ZED camera
def initialize_zed():
    zed = sl.Camera()

    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080  # Set resolution
    init_params.depth_mode = sl.DEPTH_MODE.NONE  # We don't need depth for photo capture

    if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
        print("Error: Unable to open ZED camera")
        exit()

    return zed


# Capture an image from the ZED camera
def capture_image(zed, save_directory, count):
    image = sl.Mat()

    if zed.grab() == sl.ERROR_CODE.SUCCESS:
        zed.retrieve_image(image, sl.VIEW.LEFT)  # Get the left image of the stereo camera
        image_np = image.get_data()  # Convert to numpy array

        # Create the filename for the image
        filename = os.path.join(save_directory, f"captured_image_{count}.png")

        # Save the image using OpenCV
        cv2.imwrite(filename, image_np)
        print(f"Image saved: {filename}")


# Main function to handle capturing
def main():
    # Initialize the ZED camera
    zed = initialize_zed()

    # Directory to save captured photos
    save_directory = "captured_photos_zed"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    count = 1  # Image counter

    print("Press Space to capture a photo. Press 'q' to quit.")

    while True:
        # Retrieve and display the current image for live view
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            image = sl.Mat()
            zed.retrieve_image(image, sl.VIEW.LEFT)
            img_np = image.get_data()

            # Display the image in a window
            cv2.imshow('ZED Camera', img_np)

            # Wait for a key press (1 ms delay)
            key = cv2.waitKey(1) & 0xFF

            if key == ord(' '):  # Space bar ASCII code is 32
                # Capture photo when Space is pressed
                capture_image(zed, save_directory, count)
                count += 1  # Increment image count
            elif key == ord('q'):
                # Exit when 'q' is pressed
                print("Exiting...")
                break

    # Close the ZED camera and the display window
    zed.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
