import logging
import os
from datetime import datetime
from src.utils.file_conversion import file_to_markdown
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Ensure your OpenAI API key is set in your environment variables or config


def process_resume(file_path, resume_collection):
    try:
        file_name, file_extension = os.path.splitext(file_path)
        file_type = file_extension[1:]
        markdown_content = file_to_markdown(file_path, file_type)

        # Enhancing the resume content using OpenAI API
        response = client.completions.create(engine="text-davinci-003",
        prompt=f"Enhance the following resume content:\n\n{markdown_content}",
        max_tokens=500)
        enhanced_content = response.choices[0].text.strip()

        # Add enhanced resume to Chroma DB
        resume_collection.add(
            documents=[enhanced_content],
            metadatas=[{"type": "main_resume"}],
            ids=[f"main_resume_{datetime.now().strftime('%Y%m%d%H%M%S')}"]
        )
        logging.info(f"Resume uploaded: {file_path}")
        return enhanced_content
    except Exception as e:
        logging.error(f"Error processing resume: {str(e)}")
        return None
