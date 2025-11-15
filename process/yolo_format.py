import os
from process.config import OUTPUT_YOLO_DIR

class YoloFormatter:
    @staticmethod
    def generate_yolo_label(word_boxes, filename, image_width, image_height):
        """
        Generate YOLO format label file
        Args:
            word_boxes: List of word box dictionaries
            filename: Base filename (without extension)
            image_width: Width of the image
            image_height: Height of the image
        """
        yolo_lines = []
        
        for word_data in word_boxes:
            xmin, ymin, xmax, ymax = word_data['bbox']
            
            # Convert to YOLO format (normalized center x, center y, width, height)
            x_center = ((xmin + xmax) / 2) / image_width
            y_center = ((ymin + ymax) / 2) / image_height
            width = (xmax - xmin) / image_width
            height = (ymax - ymin) / image_height
            
            # Class 0 for all words
            yolo_lines.append(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
        
        # Write YOLO label file
        yolo_path = os.path.join(OUTPUT_YOLO_DIR, f"{filename}.txt")
        with open(yolo_path, "w", encoding="utf-8") as f:
            f.write("\n".join(yolo_lines))
        
        return yolo_path