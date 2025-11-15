import os

# === CONFIG ===
TEXT_FILE = "combine_clean.txt"
FONT_DIR = "fonts"  # Folder containing all .ttf fonts
OUTPUT_IMAGE_DIR = "images"
OUTPUT_YOLO_DIR = "labels"
OUTPUT_XML_DIR = "xml_labels"

# A4 size options: Landscape (2480×1707) and Portrait (2480×3508)
DPI = 300

# Page size options
PAGE_SIZES = [
    (2480, 1707),  # Landscape - 8.27" × 5.69"
    (2480, 3508)   # Portrait - 8.27" × 11.69"
]

# Default values (will be overridden per image)
IMAGE_WIDTH = 2480
IMAGE_HEIGHT = 3508

# Margins at 300 DPI
TOP_MARGIN = 180     # 0.6" (1.5 cm) = 180 pixels
BOTTOM_MARGIN = 180  # 0.6" (1.5 cm) = 180 pixels
LEFT_MARGIN_MIN = 234   # 0.78" (2 cm) = 234 pixels
LEFT_MARGIN_MAX = 234   # Fixed left margin
RIGHT_MARGIN_MIN = 180  # 0.6" (1.5 cm) = 180 pixels
RIGHT_MARGIN_MAX = 180  # Fixed right margin

# Font and spacing
FONT_SIZE_PT = 12  # Font size in points
FONT_SIZE_MIN_PT = 9
FONT_SIZE_MAX_PT = 15

FONT_SIZE_MIN = int(FONT_SIZE_MIN_PT * DPI / 72)  
FONT_SIZE_MAX = int(FONT_SIZE_MAX_PT * DPI / 72)  

# Line spacing: 1.0 = single spacing (spacing = font size)
LINE_SPACING_MULTIPLIER = 1.0
LINE_SPACING = int((FONT_SIZE_MIN + FONT_SIZE_MAX) / 2 * LINE_SPACING_MULTIPLIER)  # ~56px

# Paragraph spacing: 6pt converted to pixels
PARAGRAPH_SPACING = int(6 * DPI / 72)  # 6pt = 25px at 300 DPI

# Images per font configuration
IMAGES_PER_FONT = 1000  # Number of images to generate per font
# Words per image configuration
MIN_WORDS_PER_IMAGE = 100
MAX_WORDS_PER_IMAGE = 2000
# === CREATE OUTPUT FOLDERS ===
os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_YOLO_DIR, exist_ok=True)
os.makedirs(OUTPUT_XML_DIR, exist_ok=True)