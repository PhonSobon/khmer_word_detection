import os

# === CONFIG ===
TEXT_FILE = "combine_clean.txt"
FONT_DIR = "fonts"  # Folder containing all .ttf fonts
OUTPUT_IMAGE_DIR = "images"
OUTPUT_YOLO_DIR = "labels"
OUTPUT_XML_DIR = "xml_labels"

# === A4 PARAMETERS (at 300 DPI) ===
# A4 size: 8.27" × 11.69" (210mm × 297mm)
DPI = 300
IMAGE_WIDTH = 2480   # 8.27" × 300 DPI = 2480 pixels
IMAGE_HEIGHT = 3508  # 11.69" × 300 DPI = 3508 pixels

# Margins at 300 DPI
TOP_MARGIN = 180     # 0.6" (1.5 cm) = 180 pixels
BOTTOM_MARGIN = 180  # 0.6" (1.5 cm) = 180 pixels
LEFT_MARGIN_MIN = 234   # 0.78" (2 cm) = 234 pixels
LEFT_MARGIN_MAX = 234   # Fixed left margin
RIGHT_MARGIN_MIN = 180  # 0.6" (1.5 cm) = 180 pixels
RIGHT_MARGIN_MAX = 180  # Fixed right margin

# Font and spacing
FONT_SIZE_PT = 12  # Font size in points
FONT_SIZE_MIN_PT = 12
FONT_SIZE_MAX_PT = 15

# Convert font size from points to pixels at 300 DPI
# Formula: pixels = points * DPI / 72
FONT_SIZE_MIN = int(FONT_SIZE_MIN_PT * DPI / 72)  # 12pt = 50px at 300 DPI
FONT_SIZE_MAX = int(FONT_SIZE_MAX_PT * DPI / 72)  # 15pt = 62px at 300 DPI

# Line spacing: 1.0 = single spacing (spacing = font size)
LINE_SPACING_MULTIPLIER = 1.0
LINE_SPACING = int((FONT_SIZE_MIN + FONT_SIZE_MAX) / 2 * LINE_SPACING_MULTIPLIER)  # ~56px

# Paragraph spacing: 6pt converted to pixels
PARAGRAPH_SPACING = int(6 * DPI / 72)  # 6pt = 25px at 300 DPI

# Images per font configuration
IMAGES_PER_FONT = 2000  # Number of images to generate per font

# === CREATE OUTPUT FOLDERS ===
os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_YOLO_DIR, exist_ok=True)
os.makedirs(OUTPUT_XML_DIR, exist_ok=True)