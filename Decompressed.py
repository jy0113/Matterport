import os
import zipfile

# 读取ID.txt文件
with open('ID.txt', 'r') as file:
    folder_ids = [line.strip() for line in file]

# 定义解压函数
def unzip_file(zip_file_path, extract_to_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_folder)

# 遍历所有文件夹并解压名为house_segmentations.zip的文件
for folder_id in folder_ids:
    folder_path = os.path.join('.', folder_id)  # 假设ID.txt与文件夹在同一目录
    zip_file_path = os.path.join(folder_path, 'house_segmentations.zip')
    
    if os.path.exists(zip_file_path):
        unzip_file(zip_file_path, folder_path)
        print(f"Decompressed done: {zip_file_path}")
    else:
        print(f"Decompressed falied: {zip_file_path}")

print("All files done")
