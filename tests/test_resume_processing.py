import unittest
from unittest.mock import patch, MagicMock
import os
from src.resume_processing import process_resume

class TestResumeProcessing(unittest.TestCase):

    def setUp(self):
        self.api_key = "test_api_key"
        self.resume_collection = MagicMock()
        self.sample_pdf = "sample_resume.pdf"
        self.sample_docx = "sample_resume.docx"
        self.sample_txt = "sample_resume.txt"
        self.sample_md = "sample_resume.md"
        # Create sample files for testing
        with open(self.sample_pdf, "w") as f:
            f.write("%PDF-1.4 sample PDF content")
        with open(self.sample_docx, "w") as f:
            f.write("Sample DOCX content")
        with open(self.sample_txt, "w") as f:
            f.write("Sample TXT content")
        with open(self.sample_md, "w") as f:
            f.write("# Sample MD content")

    def tearDown(self):
        if os.path.exists("processed_resume.md"):
            os.remove("processed_resume.md")
        # Remove sample files
        for file in [self.sample_pdf, self.sample_docx, self.sample_txt, self.sample_md]:
            if os.path.exists(file):
                os.remove(file)

    @patch('src.resume_processing.PyPDFLoader')
    @patch('src.resume_processing.OpenAIEmbeddings')
    @patch('src.resume_processing.FAISS')
    def test_process_pdf_resume(self, MockFAISS, MockEmbeddings, MockLoader):
        MockLoader().load.return_value = [MagicMock(page_content="Sample PDF content")]
        MockEmbeddings.return_value = MagicMock()
        MockFAISS.from_documents.return_value = MagicMock()
        text = process_resume(self.sample_pdf, self.api_key, self.resume_collection)
        self.assertIsNotNone(text)
        self.assertTrue(os.path.exists("processed_resume.md"))

    @patch('src.resume_processing.Docx2txtLoader')
    @patch('src.resume_processing.OpenAIEmbeddings')
    @patch('src.resume_processing.FAISS')
    def test_process_docx_resume(self, MockFAISS, MockEmbeddings, MockLoader):
        MockLoader().load.return_value = [MagicMock(page_content="Sample DOCX content")]
        MockEmbeddings.return_value = MagicMock()
        MockFAISS.from_documents.return_value = MagicMock()
        text = process_resume(self.sample_docx, self.api_key, self.resume_collection)
        self.assertIsNotNone(text)
        self.assertTrue(os.path.exists("processed_resume.md"))

    @patch('src.resume_processing.TextLoader')
    @patch('src.resume_processing.OpenAIEmbeddings')
    @patch('src.resume_processing.FAISS')
    def test_process_txt_resume(self, MockFAISS, MockEmbeddings, MockLoader):
        MockLoader().load.return_value = [MagicMock(page_content="Sample TXT content")]
        MockEmbeddings.return_value = MagicMock()
        MockFAISS.from_documents.return_value = MagicMock()
        text = process_resume(self.sample_txt, self.api_key, self.resume_collection)
        self.assertIsNotNone(text)
        self.assertTrue(os.path.exists("processed_resume.md"))

    @patch('src.resume_processing.OpenAIEmbeddings')
    @patch('src.resume_processing.FAISS')
    def test_process_md_resume(self, MockFAISS, MockEmbeddings):
        MockEmbeddings.return_value = MagicMock()
        MockFAISS.from_documents.return_value = MagicMock()
        text = process_resume(self.sample_md, self.api_key, self.resume_collection)
        self.assertIsNotNone(text)
        self.assertTrue(os.path.exists("processed_resume.md"))

if __name__ == '__main__':
    unittest.main()