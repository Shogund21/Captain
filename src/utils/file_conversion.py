import markdown2
import mammoth
from pdfminer.high_level import extract_text

def file_to_markdown(file_path, file_type):
    if file_type == 'pdf':
        text = extract_text(file_path)
        return markdown2.markdown(text)
    elif file_type == 'docx':
        with open(file_path, "rb") as docx_file:
            result = mammoth.convert_to_markdown(docx_file)
            return result.value
    elif file_type == 'txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return markdown2.markdown(content)
    elif file_type == 'md':
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    else:
        raise ValueError("Unsupported file type")
