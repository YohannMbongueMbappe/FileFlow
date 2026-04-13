import os

def rename_files(folder_path, prefix):
    for i, filename in enumerate(os.listdir(folder_path)):
        extension = filename.split('.')[-1]
        new_name = f"{prefix}_{i}.{extension}"
        os.rename(
            os.path.join(folder_path, filename),
            os.path.join(folder_path, new_name)
        )
