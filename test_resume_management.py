import unittest
from src.resume_management import ResumeManager

class TestResumeManager(unittest.TestCase):
    def setUp(self):
        self.manager = ResumeManager()

    def test_ingest_pdf(self):
        markdown_file = self.manager.ingest_resume('sample.pdf')
        self.assertTrue(os.path.exists(markdown_file))

    def test_ingest_docx(self):
        markdown_file = self.manager.ingest_resume('sample.docx')
        self.assertTrue(os.path.exists(markdown_file))

    def test_ingest_txt(self):
        markdown_file = self.manager.ingest_resume('sample.txt')
        self.assertTrue(os.path.exists(markdown_file))

    def test_ingest_md(self):
        markdown_file = self.manager.ingest_resume('sample.md')
        self.assertTrue(os.path.exists(markdown_file))

if __name__ == '__main__':
    unittest.main()
