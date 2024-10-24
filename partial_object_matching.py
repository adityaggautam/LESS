import cv2
import numpy as np

def match_partial_object(template_img, search_img):
    """
    Matches a template object (which could be partially visible) in a larger search image.
    Uses template matching to locate the object in the search image.

    :param template_img: The template image (partial object).
    :param search_img: The image in which to search for the template.
    :return: Coordinates of the best match in the search image, or None if no good match is found.
    """

    # Check if the images are valid
    if template_img is None or search_img is None:
        print("Error: One of the input images is None.")
        return None

    # Ensure both images have 3 channels
    if len(template_img.shape) != 3 or template_img.shape[2] != 3:
        print("Error: Template image must have 3 channels.")
        return None
    
    if len(search_img.shape) != 3 or search_img.shape[2] != 3:
        print("Error: Search image must have 3 channels.")
        return None

    # Convert both images to grayscale
    template_gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
    search_gray = cv2.cvtColor(search_img, cv2.COLOR_BGR2GRAY)

    # Use cv2.matchTemplate to find the location of the template in the search image
    result = cv2.matchTemplate(search_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    # Set a threshold for matching (you can adjust this value)
    threshold = 0.6

    # Get the location of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        # Get the coordinates of the top-left corner of the matched region
        top_left = max_loc
        h, w = template_gray.shape
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # Return the top-left and bottom-right corners of the matched region
        return top_left, bottom_right
    else:
        # No good match found
        print("No good match found.")
        return None
