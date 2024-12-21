import unittest
import json
from unittest.mock import patch, mock_open

# Импортируйте функции, которые хотите протестировать
from your_module import parse_value, parse_object, parse_array, parse_json

class TestJsonParser(unittest.TestCase):

    def test_parse_value_with_dict(self):
        input_data = {'key1': 'value1', 'key2': 'value2'}
        expected_output = "{\nkey1 <- value1\nkey2 <- value2\n}"
        self.assertEqual(parse_value(input_data), expected_output)

    def test_parse_value_with_list(self):
        input_data = ['value1', 'value2']
        expected_output = "#(value1,\nvalue2)"
        self.assertEqual(parse_value(input_data), expected_output)

    def test_parse_value_with_primitive(self):
        input_data = 42
        expected_output = "42"
        self.assertEqual(parse_value(input_data), expected_output)

    def test_parse_object(self):
        input_data = {'key1': 'value1', 'key2': 42}
        expected_output = "{\nkey1 <- value1\nkey2 <- 42\n}"
        self.assertEqual(parse_object(input_data), expected_output)

    def test_parse_array(self):
        input_data = ['item1', {'key': 'value'}, 3]
        expected_output = "#(item1,\n{key <- value},\n3)"
        self.assertEqual(parse_array(input_data), expected_output)

    def test_parse_json(self):
        input_data = {'name': 'John', 'age': 30, 'skills': ['Python', 'Java']}
        expected_output = "name <- John\nage <- 30\nskills <- #(Python,\nJava)"
        self.assertEqual(parse_json(input_data), expected_output)

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_main_function_valid_json(self, mock_file):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main(['script_name', 'dummy_path.json'])
            self.assertIn("key <- value", mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    def test_main_function_file_not_found(self, mock_file):
        mock_file.side_effect = FileNotFoundError
        with self.assertRaises(SystemExit):  # Verify it exits
            main(['script_name', 'non_existent_file.json'])

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": value}')  # Invalid JSON
    def test_main_function_invalid_json(self, mock_file):
        with self.assertRaises(SystemExit):  # Verify it exits
            main(['script_name', 'invalid_json.json'])

if __name__ == "__main__":
    unittest.main()