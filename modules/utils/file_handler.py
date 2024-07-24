import os
import shutil
import tempfile
import string
from datetime import datetime
from typing import List
from .archives import extract_archive

class FileHandler:
    def __init__(self):
        self.file_paths = []
        self.archive_info = []
    
    def prepare_files(self):
        all_image_paths = []
        
        for path in self.file_paths:
            if path.lower().endswith(('.cbr', '.cbz', '.zip', '.cbt', '.cb7', '.pdf', '.epub')):
                print('Extracting archive:', path)
                archive_dir = os.path.dirname(path)
                temp_dir = tempfile.mkdtemp(dir=archive_dir)
                
                extracted_files = extract_archive(path, temp_dir)
                image_paths = [f for f in extracted_files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp'))]
                image_paths = self.sanitize_and_copy_files(image_paths)
                
                all_image_paths.extend(image_paths)               
                self.archive_info.append({
                    'archive_path': path,
                    'extracted_images': image_paths,
                    'temp_dir': temp_dir
                })
            else:
                path = self.sanitize_and_copy_files([path])[0]
                all_image_paths.append(path)
        
        self.file_paths = all_image_paths
        return self.file_paths

    def sanitize_and_copy_files(self, file_paths):
        sanitized_paths = []
        for index, image_path in enumerate(file_paths):
            if not image_path.isascii():
                name = ''.join(c for c in image_path if c in string.printable)
                dir_name = ''.join(c for c in os.path.dirname(image_path) if c in string.printable)
                os.makedirs(dir_name, exist_ok=True)
                if os.path.splitext(os.path.basename(name))[1] == '':
                    basename = ""
                    ext = os.path.splitext(os.path.basename(name))[0]
                else:
                    basename = os.path.splitext(os.path.basename(name))[0]
                    ext = os.path.splitext(os.path.basename(name))[1]
                sanitized_path = os.path.join(dir_name, basename + str(index) + ext)
                try:
                    shutil.copy(image_path, sanitized_path)
                    image_path = sanitized_path
                except IOError as e:
                    print(f"An error occurred while copying or deleting the file: {e}")
            sanitized_paths.append(image_path)

        return sanitized_paths
