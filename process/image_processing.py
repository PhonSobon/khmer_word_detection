import random
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from process.config import *

class ImageGenerator:
    def __init__(self, font_manager):
        self.font_manager = font_manager
    
    def generate_image(self, words, image_count):
        """
        Generate a single image with words and return image data + word boxes
        Args:
            words: List of words to render
            image_count: Current image number
        Returns:
            tuple: (img_cv, word_boxes, words_used, font_info)
        """
        # Random parameters for this image
        font_path = self.font_manager.get_font_by_image_number(image_count)
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
        word_index = 0
        
        while word_index < len(words) and not page_full:
            word = words[word_index]
            
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
            xmin = x
            ymin = y
            xmax = bbox[2]
            ymax = bbox[3]
            
            word_boxes.append({
                'text': word,
                'bbox': (xmin, ymin, xmax, ymax),
                'line_id': line_id,
                'paragraph_id': paragraph_id
            })
            
            current_line_words.append(word)
            x += word_width
            word_index += 1
        
        # Convert PIL to OpenCV format
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        font_info = {
            'path': font_path,
            'size': font_size
        }
        
        return img_cv, word_boxes, word_index, font_info