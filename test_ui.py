import unittest
from unittest import mock
from ui import select_from_list


class TestUi(unittest.TestCase):

    @mock.patch('builtins.input')
    def test_selecting_from_an_empty_list(self, input_mock):
        self.assertEqual(select_from_list({}), '')
        self.assertEqual(input_mock.call_count, 0)

    @mock.patch('builtins.print')
    @mock.patch('builtins.input', side_effect=['not_availble', 'some_option'])
    def test_selecting_from_list_with_invalid_input(self, input_mock,
                                                    print_mock):
        options = {
            "testing": "Label for selection 1",
            "test": "Label for selection 2",
            "some_option": "Some options"
        }
        self.assertEqual(select_from_list(options), 'some_option')
        self.assertEqual(input_mock.call_count, 2)
        self.assertEqual(print_mock.call_count, 7)

    @mock.patch('builtins.print')
    @mock.patch('builtins.input')
    def test_selecting_element_from_list(self, input_mock, print_mock):
        input_mock.return_value = 'test'

        options = {
            "testing": "Label for selection 1",
            "test": "Label for selection 2",
        }
        self.assertEqual(select_from_list(options), 'test')
        self.assertEqual(input_mock.call_count, 1)
        self.assertEqual(print_mock.call_count, 2)

    @mock.patch('builtins.print')
    @mock.patch('builtins.input')
    def test_selecting_element_from_list_with_integer(self, input_mock,
                                                      print_mock):
        input_mock.return_value = '3'

        options = {f"{i}": f"Label for {i}" for i in range(5)}
        self.assertEqual(select_from_list(options), '3')
        self.assertEqual(input_mock.call_count, 1)
        self.assertEqual(print_mock.call_count, 5)


if __name__ == '__main__':
    unittest.main()
