import os
import glob

# Folder containing the files
data_folder = "kh_data_100"

# Patterns to match files to delete
patterns = [
    os.path.join(data_folder, "*_seg.txt"),
    os.path.join(data_folder, "*_seg_200b.txt")
]

# Collect all files that match the patterns
files_to_delete = []
for pattern in patterns:
    files_to_delete.extend(glob.glob(pattern))

# Delete matched files
for file_path in files_to_delete:
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Failed to delete {file_path}: {e}")

print(f"Finished deleting {len(files_to_delete)} files.")
