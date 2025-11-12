from khmernltk import word_tokenize

# Input and output file paths
input_file = "data/427022_orig.txt"
output_file = "data_clean/khmer_cleaned.txt"

# Step 1: Read text
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# Step 2: Tokenize text
tokens = word_tokenize(text)

# Step 3: Clean tokens
# Remove empty strings and extra spaces
clean_tokens = [t.strip() for t in tokens if t.strip() != ""]

# Step 4: Join tokens line by line
cleaned_text = "\n".join(clean_tokens)

# Step 5: Save result to a file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print("Cleaned text saved to", output_file)
