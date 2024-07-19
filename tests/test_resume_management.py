import unittest
import os
from src.resume_management import ResumeManager
from unittest.mock import patch

class TestResumeManagement(unittest.TestCase):
    def setUp(self):
        self.manager = ResumeManager(storage_dir='data/test_resumes')
        self.api_key = 'test_key'
        self.resume_path = 'tests/resume.md'

    @patch('src.utils.file_conversion.file_to_markdown', return_value="Markdown Content")
    def test_ingest_resume(self, mock_file_to_markdown):
        markdown_file = self.manager.ingest_resume(self.resume_path, self.api_key, None)
        self.assertTrue(os.path.exists(markdown_file))

if __name__ == '__main__':
    unittest.main()
