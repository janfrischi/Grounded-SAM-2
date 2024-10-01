import pyzed.sl as sl
import cv2
import numpy as np

def main():
    # Create a ZED camera object
    zed = sl.Camera()

    # Set initialization parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720  # Set camera resolution
    init_params.depth_mode = sl.DEPTH_MODE.NONE  # Disable depth for now, we only need RGB image
    init_params.coordinate_units = sl.UNIT.METER  # Set units to meters

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(f"Error opening ZED camera: {err}")
        exit(1)

    # Create Mat objects to hold the left and right images
    left_image = sl.Mat()
    right_image = sl.Mat()

    key = ''
    print("Press 'q' to quit the video feed.")

    while key != ord('q'):
        # Grab an image from the camera
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            # Retrieve the left and right images
            zed.retrieve_image(left_image, sl.VIEW.LEFT)
            zed.retrieve_image(right_image, sl.VIEW.RIGHT)

            # Convert the ZED Mats to NumPy arrays for OpenCV
            left_img = left_image.get_data()
            right_img = right_image.get_data()

            # Concatenate the images horizontally (left and right)
            combined_img = np.hstack((left_img, right_img))

            # Display the concatenated image using OpenCV
            cv2.imshow("ZED Stereo Camera - Left and Right Feed", combined_img)

        # Wait for key press
        key = cv2.waitKey(10)

    # Close the camera and exit
    zed.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
