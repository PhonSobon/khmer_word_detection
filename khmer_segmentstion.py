import os
import re
from khmernltk import word_tokenize

# Input and output directories
input_dir = "kh_data_100"
output_dir = "data_clean"
combine_file = os.path.join(output_dir, "combine_clean.txt")

# Create output folder if not exists
os.makedirs(output_dir, exist_ok=True)

# Prepare a list to store all combined cleaned text
all_clean_texts = []

# Loop through all files in the input folder
for filename in os.listdir(input_dir):
    if filename.endswith("_orig.txt"):
        input_path = os.path.join(input_dir, filename)
        output_filename = filename.replace("_orig.txt", "_clean.txt")
        output_path = os.path.join(output_dir, output_filename)

        # Step 1: Read text
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Step 2: Tokenize text
        tokens = word_tokenize(text)

        # Step 3: Clean tokens
        clean_tokens = []
        for t in tokens:
            t = t.strip()                     # Remove spaces
            t = re.sub(r"\.+", "", t)         # Remove ., .., ..., etc.
            t = t.replace("…", "")            # Remove unicode ellipsis

            if t != "":
                clean_tokens.append(t)

        # Step 4: Join tokens line by line
        cleaned_text = "\n".join(clean_tokens)

        # Step 5: Save result to a file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        print(f"Cleaned text saved to {output_path}")

        # Step 6: Add cleaned text to combined list
        all_clean_texts.append(cleaned_text)

# Step 7: Combine all cleaned texts into one file
with open(combine_file, "w", encoding="utf-8") as f:
    f.write("\n".join(all_clean_texts))

print("All cleaned texts combined into:", combine_file)
