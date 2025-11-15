import os
import xml.etree.ElementTree as ET
from process.config import OUTPUT_XML_DIR

class XmlFormatter:
    @staticmethod
    def generate_xml_label(word_boxes, image_name, filename, image_width, image_height):
        """
        Generate XML format label file
        Args:
            word_boxes: List of word box dictionaries
            image_name: Name of the image file
            filename: Base filename (without extension)
            image_width: Width of the image
            image_height: Height of the image
        """
        # Create root element
        root = ET.Element("metadata")
        ET.SubElement(root, "image").text = image_name
        ET.SubElement(root, "width").text = str(image_width)
        ET.SubElement(root, "height").text = str(image_height)
        
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
        xml_path = os.path.join(OUTPUT_XML_DIR, f"{filename}.xml")
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)
        
        return xml_path