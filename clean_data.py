import re
from khmernltk import word_tokenize

input_file = "combine_clean.txt"
output_file = "combine_cleaned.txt"

# Step 1: Read text
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# Step 2: Tokenize
tokens = word_tokenize(text)

clean_tokens = []
for t in tokens:

    # Strip leading/trailing spaces
    t = t.strip()
    t = re.sub(r"\.+", "", t)
    t = t.replace("…", "")  # remove unicode ellipsis

    # Remove if empty after cleaning
    if t == "":
        continue

    clean_tokens.append(t)

# Step 3: Save clean output
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(clean_tokens))

print("Cleaned text saved to", output_file)
