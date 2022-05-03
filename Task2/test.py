import unittest
from main import find_time_in_table, calendar_parser

class MyTestCase(unittest.TestCase):
    def test_find_time_in_table_1(self):
        date_list = [['2022-05-03 20:01:36', 0, 0], ['2022-05-03 20:01:36', 0, 1], ['2022-05-03 20:01:36', 0, 2], ['2022-06-30 23:59:59', 1, 1], ['2022-07-01 23:59:59', 1, 2], ['2022-07-02 13:00:00', 0, 1], ['2022-07-02 13:14:59', 1, 0], ['2022-07-02 14:00:00', 0, 0], ['2022-07-03 00:00:00', 0, 2], ['3000-01-01 00:00:00', 1, 0], ['3000-01-01 00:00:00', 1, 1], ['3000-01-01 00:00:00', 1, 2]]
        self.assertEqual(find_time_in_table(date_list, duration_in_minutes=30, min_people=3), "2022-05-03 20:01:36", "Should be 2022-05-03 20:01:36")

    def test_find_time_in_table_2(self):
        date_list = [['2022-07-01 09:00:00', 0, 0], ['2022-07-01 09:00:00', 0, 2], ['2022-07-01 23:59:59', 1, 2], ['2022-07-02 13:00:00', 0, 1], ['2022-07-02 13:14:59', 1, 0], ['2022-07-02 14:00:00', 0, 0], ['2022-07-03 00:00:00', 0, 2], ['3000-01-01 00:00:00', 1, 0], ['3000-01-01 00:00:00', 1, 1], ['3000-01-01 00:00:00', 1, 2]]
        self.assertEqual(find_time_in_table(date_list, duration_in_minutes=30, min_people=3), "2022-07-03 00:00:00", "Should be 2022-07-03 00:00:00" )

    def test_find_time_in_table_3(self):
        date_list = [['2022-07-01 09:00:00', 0, 0], ['2022-07-01 09:00:00', 0, 2], ['2022-07-01 23:59:59', 1, 2],
                     ['2022-07-02 13:00:00', 0, 1], ['2022-07-02 13:14:59', 1, 0], ['2022-07-02 14:00:00', 0, 0],
                     ['2022-07-03 00:00:00', 0, 2], ['3000-01-01 00:00:00', 1, 0], ['3000-01-01 00:00:00', 1, 1],
                     ['3000-01-01 00:00:00', 1, 2]]
        self.assertEqual(find_time_in_table(date_list, duration_in_minutes=30, min_people=2), "2022-07-01 09:00:00",
                         "Should be 2022-07-01 09:00:00")

    def test_find_time_in_table_4(self):
        date_list = [['2022-07-01 09:00:00', 0, 0], ['2022-07-02 13:00:00', 0, 1], ['2022-07-02 13:14:59', 1, 0], ['2022-07-02 14:00:00', 0, 0],['3000-01-01 00:00:00', 1, 0], ['3000-01-01 00:00:00', 1, 1]]
        self.assertEqual(find_time_in_table(date_list, duration_in_minutes=30, min_people=2), "2022-07-02 14:00:00",
                         "Should be 2022-07-02 14:00:00")

    def test_find_time_in_table_5(self):
        date_list = [['2022-07-01 09:00:00', 0, 0], ['2022-07-02 13:00:00', 0, 1], ['2022-07-02 13:14:59', 1, 0], ['2022-07-02 14:00:00', 0, 0],['3000-01-01 00:00:00', 1, 0], ['3000-01-01 00:00:00', 1, 1]]
        self.assertEqual(find_time_in_table(date_list, duration_in_minutes=14, min_people=2), "2022-07-02 13:00:00",
                         "Should be 2022-07-02 13:00:00")

    def test_calendar_parser_1(self):
        date_list = []
        calendar = ["2022-07-01", "2022-07-02 00:00:00 - 2022-07-02 12:59:59"]
        calendar_parser(date_list, date_lines=calendar, index=0, date_now="2022-06-01 00:00:00")
        ans_list = [["2022-06-01 00:00:00", 0, 0], ["2022-06-30 23:59:59", 1, 0], ["2022-07-02 13:00:00", 0, 0], ["3000-01-01 00:00:00", 1, 0]]
        self.assertEqual(date_list, ans_list, "Wrong parsing")

    def test_calendar_parser_2(self):
        date_list = []
        calendar = ["2022-07-01", "2022-07-02 00:00:00 - 2022-07-02 12:59:59"]
        calendar_parser(date_list, date_lines=calendar, index=0, date_now="2022-07-01 09:00:00")
        ans_list = [["2022-07-02 13:00:00", 0, 0], ["3000-01-01 00:00:00", 1, 0]]
        self.assertEqual(date_list, ans_list, "Wrong parsing")


if __name__ == '__main__':
    unittest.main()
