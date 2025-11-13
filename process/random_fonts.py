import os
from process.config import FONT_DIR

class FontManager:
    def __init__(self):
        self.all_fonts = []
        self.load_fonts()
    
    def load_fonts(self):
        """Load all .ttf fonts from FONT_DIR"""
        self.all_fonts = sorted([
            os.path.join(FONT_DIR, f) 
            for f in os.listdir(FONT_DIR) 
            if f.endswith(".ttf")
        ])
        
        if not self.all_fonts:
            raise Exception(f"No .ttf fonts found in {FONT_DIR} folder!")
        
        print(f"Loaded {len(self.all_fonts)} fonts from {FONT_DIR}")
        for i, font_path in enumerate(self.all_fonts, 1):
            print(f"  {i}. {os.path.basename(font_path)}")
    
    def get_all_fonts(self):
        """Return list of all font paths"""
        return self.all_fonts
    
    def get_font_count(self):
        """Return total number of fonts"""
        return len(self.all_fonts)
    
    def get_font_name(self, font_path):
        """Get font filename without extension"""
        return os.path.splitext(os.path.basename(font_path))[0]