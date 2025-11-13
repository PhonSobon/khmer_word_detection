import os
import cv2
import random
from process.config import TEXT_FILE, OUTPUT_IMAGE_DIR, IMAGES_PER_FONT, FONT_SIZE_MIN, FONT_SIZE_MAX
from process.random_fonts import FontManager
from process.image_processing import ImageGenerator
from process.yolo_format import YoloFormatter
from process.xml_format import XmlFormatter

def main():
    """
    Main function to generate images with YOLO and XML annotations
    Generates specified number of images per font
    """
    print("=" * 70)
    print("KHMER TEXT IMAGE GENERATOR (Font-Based Generation)")
    print("=" * 70)
    
    # Initialize components
    print("\n[1] Initializing Font Manager...")
    font_manager = FontManager()
    all_fonts = font_manager.get_all_fonts()
    total_fonts = font_manager.get_font_count()
    
    print("\n[2] Initializing Image Generator...")
    image_generator = ImageGenerator(font_manager)
    
    print("\n[3] Loading Khmer text data...")
    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        all_words = [line.strip() for line in f if line.strip()]
    print(f"Loaded {len(all_words)} words from {TEXT_FILE}")
    
    # Initialize formatters
    yolo_formatter = YoloFormatter()
    xml_formatter = XmlFormatter()
    
    # Calculate total images to generate
    total_images = total_fonts * IMAGES_PER_FONT
    print(f"\n[4] Generation Plan:")
    print(f"    Total fonts: {total_fonts}")
    print(f"    Images per font: {IMAGES_PER_FONT}")
    print(f"    Total images to generate: {total_images}")
    
    # Generate images
    print("\n[5] Starting image generation...")
    print("-" * 70)
    
    overall_image_count = 0
    total_words_processed = 0
    word_index = 0
    
    # Generate images for each font
    for font_idx, font_path in enumerate(all_fonts, 1):
        font_name = font_manager.get_font_name(font_path)
        
        print(f"\n--- Font {font_idx}/{total_fonts}: {font_name} ---")
        
        for img_num in range(1, IMAGES_PER_FONT + 1):
            overall_image_count += 1
            
            # Reset to beginning of words if we run out
            if word_index >= len(all_words):
                word_index = 0
            
            # Get remaining words to process
            remaining_words = all_words[word_index:]
            
            # Random font size for each image
            font_size = random.randint(FONT_SIZE_MIN, FONT_SIZE_MAX)
            
            # Generate image
            img_cv, word_boxes, words_used = image_generator.generate_image(
                remaining_words, 
                font_path,
                font_size
            )
            
            # Create unique filename with zero-padded numbering
            output_filename = f"img_{overall_image_count:05d}"
            image_name = f"{output_filename}.png"
            image_path = os.path.join(OUTPUT_IMAGE_DIR, image_name)
            
            # Save image
            cv2.imwrite(image_path, img_cv)
            
            # Generate YOLO label
            yolo_formatter.generate_yolo_label(word_boxes, output_filename)
            
            # Generate XML label
            xml_formatter.generate_xml_label(word_boxes, image_name, output_filename)
            
            # Update statistics
            word_index += words_used
            total_words_processed += len(word_boxes)
            
            # Print progress every 500 images or on first/last of each font
            if img_num == 1 or img_num == IMAGES_PER_FONT or img_num % 500 == 0:
                progress = (overall_image_count / total_images) * 100
                print(f"  [{progress:5.1f}%] Image {img_num:4d}/{IMAGES_PER_FONT} | "
                      f"Words: {len(word_boxes):3d} | Size: {font_size}pt | "
                      f"File: {output_filename}.png")
    
    # Final summary
    print("\n" + "-" * 70)
    print("\n[6] Generation Complete!")
    print(f"    Total fonts processed: {total_fonts}")
    print(f"    Images per font: {IMAGES_PER_FONT}")
    print(f"    Total images generated: {overall_image_count}")
    print(f"    Total words processed: {total_words_processed}")
    print(f"    Word recycling cycles: {word_index // len(all_words)}")
    print(f"\n    Output directories:")
    print(f"      - Images: {OUTPUT_IMAGE_DIR}/")
    print(f"      - YOLO labels: labels/")
    print(f"      - XML labels: xml_labels/")
    print("=" * 70)
    
    # Print per-font summary
    print("\n[7] Per-Font Summary:")
    for font_idx, font_path in enumerate(all_fonts, 1):
        font_name = font_manager.get_font_name(font_path)
        print(f"  {font_idx:2d}. {font_name:40s} - {IMAGES_PER_FONT} images")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()