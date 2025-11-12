import os
import random
from process.config import FONT_DIR

class FontManager:
    def __init__(self):
        self.odd_fonts = []
        self.even_fonts = []
        self.load_fonts()
    
    def load_fonts(self):
        """Load all .ttf fonts from FONT_DIR and split into odd/even lists"""
        all_fonts = [os.path.join(FONT_DIR, f) for f in os.listdir(FONT_DIR) if f.endswith(".ttf")]
        
        if not all_fonts:
            raise Exception(f"No .ttf fonts found in {FONT_DIR} folder!")
        
        # Split fonts into odd and even indexed lists
        for i, font_path in enumerate(all_fonts):
            if i % 2 == 0:
                self.even_fonts.append(font_path)
            else:
                self.odd_fonts.append(font_path)
        
        print(f"Loaded {len(all_fonts)} fonts from {FONT_DIR}")
        print(f"  - Odd fonts: {len(self.odd_fonts)}")
        print(f"  - Even fonts: {len(self.even_fonts)}")
    
    def get_random_font(self, use_odd=None):
        """
        Get a random font from odd or even list
        Args:
            use_odd: If True, select from odd fonts. If False, select from even fonts.
                     If None, randomly choose odd or even.
        Returns:
            Path to a random font file
        """
        if use_odd is None:
            use_odd = random.choice([True, False])
        
        if use_odd and self.odd_fonts:
            return random.choice(self.odd_fonts)
        elif not use_odd and self.even_fonts:
            return random.choice(self.even_fonts)
        else:
            # Fallback if one list is empty
            return random.choice(self.odd_fonts + self.even_fonts)
    
    def get_font_by_image_number(self, image_number):
        """
        Get font based on image number (odd image = odd font, even image = even font)
        Args:
            image_number: The current image count
        Returns:
            Path to a font file
        """
        use_odd = (image_number % 2 == 1)
        return self.get_random_font(use_odd=use_odd)