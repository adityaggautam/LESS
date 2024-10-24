import numpy as np

# Define color ranges for detection (can be adjusted as needed)
color_ranges = {
    'red': ([0, 0, 100], [50, 50, 255]),  # BGR format
    'green': ([0, 100, 0], [50, 255, 50]),
    'blue': ([100, 0, 0], [255, 50, 50]),
    'yellow': ([0, 100, 100], [50, 255, 255]),
    'orange': ([0, 50, 100], [100, 150, 255]),
    'black': ([0, 0, 0], [50, 50, 50]),
    'white': ([200, 200, 200], [255, 255, 255]),
}

def detect_color_name(dominant_color):
    """
    Detects and returns the name of the closest matching color based on BGR values.
    
    :param dominant_color: List or array of BGR values for the detected color.
    :return: Name of the closest matching color as a string.
    """
    b, g, r = dominant_color
    for color_name, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        if np.all(lower <= [b, g, r]) and np.all([b, g, r] <= upper):
            return color_name
    return "unknown"
