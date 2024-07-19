import os
from src.utils.file_conversion import file_to_markdown

class ResumeManager:
    def __init__(self, storage_dir='data/resumes'):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def ingest_resume(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        file_type = file_extension[1:]
        markdown_content = file_to_markdown(file_path, file_type)
        markdown_file = os.path.join(self.storage_dir, f"{os.path.basename(file_name)}.md")
        with open(markdown_file, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        return markdown_file
