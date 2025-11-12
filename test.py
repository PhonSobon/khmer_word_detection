import os
import cv2
import random
import numpy as np
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

# === CONFIG ===
TEXT_FILE = "data_clean/khmer_cleaned.txt"
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
FONT_SIZE_MAX = 13
LINE_SPACING = 8
WORD_SPACING = 5  # Single space between words

# === CREATE OUTPUT FOLDERS ===
os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_YOLO_DIR, exist_ok=True)
os.makedirs(OUTPUT_XML_DIR, exist_ok=True)

# === LOAD FONTS FROM FOLDER ===
FONTS = [os.path.join(FONT_DIR, f) for f in os.listdir(FONT_DIR) if f.endswith(".ttf")]
if not FONTS:
    raise Exception(f"No .ttf fonts found in {FONT_DIR} folder!")

print(f"🧩 Loaded {len(FONTS)} fonts from {FONT_DIR}")

# === READ KHMER CLEANED TEXT ===
with open(TEXT_FILE, "r", encoding="utf-8") as f:
    all_words = [line.strip() for line in f if line.strip()]

# === GENERATE IMAGES ===
image_count = 0
word_index = 0

while word_index < len(all_words):
    image_count += 1
    
    # Random parameters for this image
    font_path = random.choice(FONTS)
    font_size = random.randint(FONT_SIZE_MIN, FONT_SIZE_MAX)
    left_margin = random.randint(LEFT_MARGIN_MIN, LEFT_MARGIN_MAX)
    right_margin = random.randint(RIGHT_MARGIN_MIN, RIGHT_MARGIN_MAX)
    
    font = ImageFont.truetype(font_path, font_size)
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Calculate usable width
    usable_width = IMAGE_WIDTH - left_margin - right_margin
    
    x, y = left_margin, TOP_MARGIN
    word_boxes = []
    line_id = 1
    paragraph_id = 1
    current_line_words = []
    
    # Fill the page with words
    page_full = False
    while word_index < len(all_words) and not page_full:
        word = all_words[word_index]
        
        # Get word dimensions
        bbox = draw.textbbox((x, y), word, font=font)
        word_width = bbox[2] - bbox[0]
        word_height = bbox[3] - bbox[1]
        
        # Check if word fits on current line
        if x + word_width > left_margin + usable_width:
            # Move to next line
            if current_line_words:
                line_id += 1
            current_line_words = []
            y += word_height + LINE_SPACING
            x = left_margin
            
            # Check if we've reached bottom margin
            if y + word_height > IMAGE_HEIGHT - BOTTOM_MARGIN:
                page_full = True
                break
            
            # Recalculate bbox for new position
            bbox = draw.textbbox((x, y), word, font=font)
            word_width = bbox[2] - bbox[0]
            word_height = bbox[3] - bbox[1]
        
        # Draw the word
        draw.text((x, y), word, font=font, fill=(0, 0, 0))
        
        # Store word info
        xmin, ymin = x, y
        xmax, ymax = x + word_width, y + word_height
        word_boxes.append({
            'text': word,
            'bbox': (xmin, ymin, xmax, ymax),
            'line_id': line_id,
            'paragraph_id': paragraph_id
        })
        
        current_line_words.append(word)
        x += word_width + WORD_SPACING
        word_index += 1
    
    # Convert PIL to OpenCV format
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    image_name = f"kh_data_{image_count}.png"
    image_path = os.path.join(OUTPUT_IMAGE_DIR, image_name)
    cv2.imwrite(image_path, img_cv)
    
    # === GENERATE YOLO LABEL ===
    yolo_lines = []
    for word_data in word_boxes:
        xmin, ymin, xmax, ymax = word_data['bbox']
        x_center = ((xmin + xmax) / 2) / IMAGE_WIDTH
        y_center = ((ymin + ymax) / 2) / IMAGE_HEIGHT
        width = (xmax - xmin) / IMAGE_WIDTH
        height = (ymax - ymin) / IMAGE_HEIGHT
        yolo_lines.append(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    
    with open(os.path.join(OUTPUT_YOLO_DIR, f"kh_data_{image_count}.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(yolo_lines))
    
    # === GENERATE XML LABEL (matching your format) ===
    root = ET.Element("metadata")
    ET.SubElement(root, "image").text = image_name
    ET.SubElement(root, "width").text = str(IMAGE_WIDTH)
    ET.SubElement(root, "height").text = str(IMAGE_HEIGHT)
    
    # Group words by paragraph and line
    paragraphs = {}
    for word_data in word_boxes:
        para_id = word_data['paragraph_id']
        line_id = word_data['line_id']
        
        if para_id not in paragraphs:
            paragraphs[para_id] = {}
        if line_id not in paragraphs[para_id]:
            paragraphs[para_id][line_id] = []
        
        paragraphs[para_id][line_id].append(word_data)
    
    # Build XML structure
    for para_id in sorted(paragraphs.keys()):
        paragraph = ET.SubElement(root, "paragraph")
        if para_id > 0:
            paragraph.set("id", str(para_id))
        
        for line_id in sorted(paragraphs[para_id].keys()):
            line = ET.SubElement(paragraph, "line", id=str(line_id))
            
            for word_data in paragraphs[para_id][line_id]:
                word_elem = ET.SubElement(line, "word")
                text_elem = ET.SubElement(word_elem, "text")
                text_elem.text = word_data['text']
                
                xmin, ymin, xmax, ymax = word_data['bbox']
                bbox_elem = ET.SubElement(word_elem, "bbox")
                bbox_elem.set("x1", str(int(xmin)))
                bbox_elem.set("y1", str(int(ymin)))
                bbox_elem.set("x2", str(int(xmax)))
                bbox_elem.set("y2", str(int(ymax)))
    
    # Write XML file
    tree = ET.ElementTree(root)
    ET.indent(tree, space="", level=0)  # Python 3.9+
    xml_path = os.path.join(OUTPUT_XML_DIR, f"kh_data_{image_count}.xml")
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    
    print(f"✅ Generated {image_name} ({len(word_boxes)} words) using {os.path.basename(font_path)} size {font_size}")

print(f"\n🎉 Generated {image_count} images with YOLO and XML annotations!")
print(f"📊 Total words processed: {word_index}/{len(all_words)}")