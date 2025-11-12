import os
import cv2
from process.config import TEXT_FILE, OUTPUT_IMAGE_DIR
from process.random_fonts import FontManager
from process.image_processing import ImageGenerator
from process.yolo_format import YoloFormatter
from process.xml_format import XmlFormatter

def main():
    """
    Main function to generate images with YOLO and XML annotations
    """
    print("=" * 60)
    print("KHMER TEXT IMAGE GENERATOR")
    print("=" * 60)
    
    # Initialize components
    print("\n[1] Initializing Font Manager...")
    font_manager = FontManager()
    
    print("\n[2] Initializing Image Generator...")
    image_generator = ImageGenerator(font_manager)
    
    print("\n[3] Loading Khmer text data...")
    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        all_words = [line.strip() for line in f if line.strip()]
    print(f"Loaded {len(all_words)} words from {TEXT_FILE}")
    
    # Initialize formatters
    yolo_formatter = YoloFormatter()
    xml_formatter = XmlFormatter()
    
    # Generate images
    print("\n[4] Starting image generation...")
    print("-" * 60)
    
    image_count = 0
    word_index = 0
    
    while word_index < len(all_words):
        image_count += 1
        
        # Get remaining words to process
        remaining_words = all_words[word_index:]
        
        # Generate image
        img_cv, word_boxes, words_used, font_info = image_generator.generate_image(
            remaining_words, 
            image_count
        )
        
        # Save image
        image_name = f"kh_data_{image_count}.png"
        image_path = os.path.join(OUTPUT_IMAGE_DIR, image_name)
        cv2.imwrite(image_path, img_cv)
        
        # Generate YOLO label
        yolo_formatter.generate_yolo_label(word_boxes, image_count)
        
        # Generate XML label
        xml_formatter.generate_xml_label(word_boxes, image_name, image_count)
        
        # Update word index
        word_index += words_used
        
        # Print progress
        font_type = "ODD" if image_count % 2 == 1 else "EVEN"
        font_name = os.path.basename(font_info['path'])
        print(f"✓ Image {image_count:4d} | Words: {len(word_boxes):4d} | "
              f"Font: [{font_type}] {font_name} (size {font_info['size']})")
    
    # Final summary
    print("-" * 60)
    print("\n[5] Generation Complete!")
    print(f"    Total images generated: {image_count}")
    print(f"    Total words processed: {word_index}/{len(all_words)}")
    print(f"    Output directories:")
    print(f"      - Images: {OUTPUT_IMAGE_DIR}")
    print(f"      - YOLO labels: {os.path.join(OUTPUT_IMAGE_DIR, '../labels')}")
    print(f"      - XML labels: {os.path.join(OUTPUT_IMAGE_DIR, '../xml_labels')}")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        raise