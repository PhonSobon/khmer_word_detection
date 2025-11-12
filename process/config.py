import os

# === CONFIG ===
TEXT_FILE = "combine_clean.txt"
FONT_DIR = "fonts"  # Folder containing all .ttf fonts
OUTPUT_IMAGE_DIR = "images"
OUTPUT_YOLO_DIR = "labels"
OUTPUT_XML_DIR = "xml_labels"

# === A4 PARAMETERS (at 96 DPI) ===
# A4 size: 210mm x 297mm
DPI = 96
IMAGE_WIDTH = int(210 * DPI / 25.4)   # ~794 pixels
IMAGE_HEIGHT = int(297 * DPI / 25.4)  # ~1123 pixels

# Margins in cm converted to pixels
LEFT_MARGIN_MIN = int(1.8 * DPI / 2.54)   # ~68 pixels
LEFT_MARGIN_MAX = int(2.0 * DPI / 2.54)   # ~76 pixels
RIGHT_MARGIN_MIN = int(1.5 * DPI / 2.54)  # ~57 pixels
RIGHT_MARGIN_MAX = int(1.8 * DPI / 2.54)  # ~68 pixels
TOP_MARGIN = int(1.5 * DPI / 2.54)        # ~57 pixels
BOTTOM_MARGIN = int(1.5 * DPI / 2.54)     # ~57 pixels

# Font and spacing
FONT_SIZE_MIN = 9
FONT_SIZE_MAX = 30
LINE_SPACING = 8
WORD_SPACING = 5  # Single space between words

# === CREATE OUTPUT FOLDERS ===
os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_YOLO_DIR, exist_ok=True)
os.makedirs(OUTPUT_XML_DIR, exist_ok=True)