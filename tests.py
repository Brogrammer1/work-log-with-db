import unittest
import workLog2
import datetime
from unittest.mock import patch


class TestWorkLogMethods(unittest.TestCase):

    def test_view_entries(self):
        self.assertEqual(workLog2.view_entries(),
                         workLog2.Task.select().order_by(
                             workLog2.Task.timestamp.desc()))

    def test_entry_instance(self):
        self.assertIsInstance(workLog2.view_entries()[0], workLog2.Task)

    def test_find_employee(self):
        self.assertEqual(
            workLog2.search_by_employee('Curtis')[0].employee_name,
            'Curtis')

    def test_find_by_time(self):
        self.assertEqual(
            workLog2.search_by_time('5')[0].time_worked,
            5)

    def test_find_by_date(self):
        self.assertEqual(
            workLog2.search_by_date('11/07/2018')[0].timestamp,
            datetime.date(2018, 7, 11)
        )

    def test_search_by_task_or_notes(self):
        self.assertIn('yes',
                      workLog2.search_by_task_or_notes('yes')[0].general_notes)
        self.assertIn('py',
                      workLog2.search_by_task_or_notes('py')[0].task_name)

    def test_add_entry(self):
        with unittest.mock.patch('builtins.input', return_value='y'):
            assert workLog2.add_entry('jimmy', '900', 'work',
                                      'yesss') == print("Saved successfully!")

    def test_delete_entry(self):
        with unittest.mock.patch('builtins.input', return_value='y'):
            assert workLog2.delete_entry(
                workLog2.search_by_employee('jimmy')[0]) == print(
                "Entry deleted!")


if __name__ == '__main__':
    workLog2.initialize()
    unittest.main()
