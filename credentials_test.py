import unittest
from credentials import get_credentials
from unittest.mock import patch, mock_open, call


class MyTestCase(unittest.TestCase):

    @patch('os.path')
    @patch("builtins.open", mock_open(read_data='http://abc\ntest\npassword'))
    def test_reading_credentials_from_file(self, mock_os_path):
        # Setting up the mocks
        mock_os_path.exists.return_value = True

        # Doing the real call
        self.assertEqual(get_credentials(), ['http://abc', 'test', 'password'])

        # Asserting functions have been called
        mock_os_path.exists.assert_called_once_with('.env')
        open.assert_called_once_with('.env')

    @patch('os.path')
    @patch('builtins.input', return_value="abcs")
    @patch("builtins.open", create=True)
    def test_reading_credentials_from_command_line(self, mock_file, mock_input,
                                                   mock_os_path):
        # Setting up the mocks
        mock_os_path.exists.return_value = False

        # Doing the real call
        self.assertEqual(get_credentials(), ['abcs', 'abcs', 'abcs'])

        # Asserting functions have been called
        mock_os_path.exists.assert_called_once_with('.env')
        mock_file.assert_called_once_with('.env', 'w')
        mock_file().write.assert_has_calls(
            [call('abcs\n'), call('abcs\n'),
             call('abcs')])
        self.assertEqual(mock_file().write.call_count, 3)
        mock_file().close.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
