import unittest
from unittest.mock import patch, MagicMock
import directory as directory

class TestDirectoryEnumerationTool(unittest.TestCase):

    @patch('directory.requests')
    @patch('directory.time')
    def test_enumerate_directories(self, mock_time, mock_requests):
        mock_time.time.return_value = 0  
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.head.return_value = mock_response

        root = MagicMock()
        app = directory.enumerate_directories()  

       

if __name__ == '__main__':
    unittest.main()
