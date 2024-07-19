import unittest
from src.job_tracking import JobTracker

class TestJobTracking(unittest.TestCase):
    def setUp(self):
        self.tracker = JobTracker(':memory:')  # Use in-memory database for testing

    def test_add_application(self):
        self.tracker.add_application('Company A', 'Position A', '2023-07-16', 'Applied')
        applications = self.tracker.get_applications()
        self.assertEqual(len(applications), 1)

    def test_update_application_status(self):
        self.tracker.add_application('Company B', 'Position B', '2023-07-16', 'Applied')
        applications = self.tracker.get_applications()
        app_id = applications[0][0]  # Assuming id is the first field
        self.tracker.update_application_status(app_id, 'Interviewing')
        applications = self.trtracker.get_applications()
        self.assertEqual(applications[0][4], 'Interviewing')

if __name__ == '__main__':
    unittest.main()
