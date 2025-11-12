import os
from process.config import IMAGE_WIDTH, IMAGE_HEIGHT, OUTPUT_YOLO_DIR

class YoloFormatter:
    @staticmethod
    def generate_yolo_label(word_boxes, image_count):
        """
        Generate YOLO format label file
        Args:
            word_boxes: List of word box dictionaries
            image_count: Current image number
        """
        yolo_lines = []
        
        for word_data in word_boxes:
            xmin, ymin, xmax, ymax = word_data['bbox']
            
            # Convert to YOLO format (normalized center x, center y, width, height)
            x_center = ((xmin + xmax) / 2) / IMAGE_WIDTH
            y_center = ((ymin + ymax) / 2) / IMAGE_HEIGHT
            width = (xmax - xmin) / IMAGE_WIDTH
            height = (ymax - ymin) / IMAGE_HEIGHT
            
            # Class 0 for all words
            yolo_lines.append(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
        
        # Write YOLO label file
        yolo_path = os.path.join(OUTPUT_YOLO_DIR, f"kh_data_{image_count}.txt")
        with open(yolo_path, "w", encoding="utf-8") as f:
            f.write("\n".join(yolo_lines))
        
        return yolo_path