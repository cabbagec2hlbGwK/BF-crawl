import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def on_trackbar_change(_=None):
    # If the trackbars do not exist, the following lines will raise an error
    contrast = cv2.getTrackbarPos('Contrast', 'Adjustments') / 10
    brightness = cv2.getTrackbarPos('Brightness', 'Adjustments') - 100
    hue = cv2.getTrackbarPos('Hue', 'Adjustments') - 100
    saturation = cv2.getTrackbarPos('Saturation', 'Adjustments') / 10
    gamma = max(cv2.getTrackbarPos('Gamma', 'Adjustments') / 10, 0.1)
    print(f"Contrast:{contrast}, Brightness:{brightness}, Hue:{hue}, Saturation:{saturation}, Gama:{gamma}")

    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    hsv_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv_image[..., 0] = (hsv_image[..., 0] + hue) % 180
    hsv_image[..., 1] = hsv_image[..., 1] * saturation
    hsv_image = np.clip(hsv_image, 0, 255).astype(np.uint8)
    adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    
    adjusted_image = adjust_gamma(adjusted_image, gamma=gamma)
    cv2.imshow('Adjustments', adjusted_image)

# Load the image
image_path = 'captas/12070a4c-3fb6-4cb0-ac62-668f2cd18f63.jpg'
image = cv2.imread(image_path)
if image is None:
    print("Error: Image not found. Check the image path.")
    exit()

# Create a window and show the initial image
cv2.namedWindow('Adjustments')
cv2.imshow('Adjustments', image)

# Create trackbars for adjustments
cv2.createTrackbar('Contrast', 'Adjustments', 10, 30, on_trackbar_change)
cv2.createTrackbar('Brightness', 'Adjustments', 100, 200, on_trackbar_change)
cv2.createTrackbar('Hue', 'Adjustments', 100, 200, on_trackbar_change)
cv2.createTrackbar('Saturation', 'Adjustments', 10, 30, on_trackbar_change)
cv2.createTrackbar('Gamma', 'Adjustments', 10, 30, on_trackbar_change)

# Explicitly call the function to ensure everything is initialized
on_trackbar_change()

cv2.waitKey(0)
cv2.destroyAllWindows()
