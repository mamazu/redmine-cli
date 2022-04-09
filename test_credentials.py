import unittest
from credentials import get_credentials
from unittest.mock import patch, mock_open, call


class MyTestCase(unittest.TestCase):

    @patch('os.path')
    @patch("builtins.open", mock_open(read_data='http://redmine.com\ntest\npassword'))
    def test_reading_credentials_from_file(self, mock_os_path):
        # Setting up the mocks
        mock_os_path.exists.return_value = True

        # Doing the real call
        self.assertEqual(get_credentials('.env'), ['http://redmine.com', 'test', 'password'])

        # Asserting functions have been called
        mock_os_path.exists.assert_called_once_with('.env')
        open.assert_called_once_with('.env')

    @patch('getpass.getpass')
    @patch('builtins.input', side_effect=['http://redmine.com', 'username' ])
    @patch('os.path')
    @patch("builtins.open", create=True)
    def test_reading_credentials_from_command_line(self, mock_file, mock_os_path, mock_input, password_prompt_mock):
        # Setting up the mocks
        mock_os_path.exists.return_value = False
        password_prompt_mock.return_value = 'password'

        # Doing the real call
        self.assertEqual(
                get_credentials('.env'),
                ['http://redmine.com', 'username', 'password']
                )

        # Asserting functions have been called
        mock_os_path.exists.assert_called_once_with('.env')
        mock_file.assert_called_once_with('.env', 'w')
        mock_file().write.assert_has_calls(
            [call('http://redmine.com\nusername\npassword')])
        self.assertEqual(mock_file().write.call_count, 1)
        self.assertEqual(mock_input.call_count, 2)
        mock_file().close.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
