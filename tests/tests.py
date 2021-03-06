import unittest
import os
from unittest.mock import patch
from django_easy_drf.main import create_all
from django_easy_drf.errors import InvalidModelError


FILES = ['serializers.py', 'views.py', 'urls.py']

class FileTestMixin:
    def assertFile(self, folder, expected_path, actual_path):
        with open(os.path.join(folder, 'expected_files/', expected_path), 'r') as expected_file:
            with open(os.path.join(folder, actual_path), 'r') as actual_file:
                actual_lines = actual_file.read().splitlines()
                expected_lines = expected_file.read().splitlines()
                for line_index in range(0, len(expected_lines)):
                    self.assertEqual(expected_lines[line_index], actual_lines[line_index])

    def tearDown(self):
        for file in FILES:
            file_path = os.path.join(self.get_test_folder(), file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def get_test_folder(self):
        return os.path.dirname(os.path.abspath(__file__))

class CreateAllFilesTest(FileTestMixin, unittest.TestCase):

    def test_create_all_creates_serializers_file_correctly(self):
        with patch('builtins.input', return_value='y') as _:
            test_folder = self.get_test_folder()

            create_all(test_folder, ['s'])

            self.assertFile(test_folder, 'serializers-expected.py', 'serializers.py')

            self.assertFalse(os.path.exists(os.path.join(test_folder, 'views.py')))
            self.assertFalse(os.path.exists(os.path.join(test_folder, 'urls.py')))

    def test_create_all_creates_views_file_correctly(self):
        with patch('builtins.input', return_value='Y') as _:
            test_folder = self.get_test_folder()

            create_all(test_folder, ['v'])

            self.assertFile(test_folder, 'views-expected.py', 'views.py')
            
            self.assertFalse(os.path.exists(os.path.join(test_folder, 'urls.py')))
            self.assertFalse(os.path.exists(os.path.join(test_folder, 'serializers.py')))

    def test_create_all_creates_urls_file_correctly(self):
        with patch('builtins.input', return_value='') as _:
            test_folder = self.get_test_folder()

            create_all(test_folder, ['u'])

            self.assertFile(test_folder, 'urls-expected.py', 'urls.py')
            
            self.assertFalse(os.path.exists(os.path.join(test_folder, 'serializers.py')))
            self.assertFalse(os.path.exists(os.path.join(test_folder, 'views.py')))

    def test_create_all_with_models_specified_only_creates_data_for_those_models(self):
        with patch('builtins.input', return_value='') as _:
            test_folder = self.get_test_folder()

            create_all(test_folder, ['u', 'v', 's'], models=['ExampleModel', 'DogModel',])

            self.assertFile(test_folder, 'urls-expected-specific-models.py', 'urls.py')
            self.assertFile(test_folder, 'serializers-expected-specific-models.py', 'serializers.py')
            self.assertFile(test_folder, 'views-expected-specific-models.py', 'views.py')

    def test_create_all_with_invalid_model_raises_error(self):
        with patch('builtins.input', return_value='') as _:
            test_folder = self.get_test_folder()

            with self.assertRaises(InvalidModelError) as context:
                create_all(test_folder, ['u', 'v', 's'], models=['InvalidModel', 'DogModel',])

            self.assertEqual('InvalidModelError: InvalidModel not found on models.py', str(context.exception))
            self.assertFalse(os.path.exists(os.path.join(test_folder, 'serializers.py')))
            self.assertFalse(os.path.exists(os.path.join(test_folder, 'views.py')))
            self.assertFalse(os.path.exists(os.path.join(test_folder, 'urls.py')))

    def test_create_all_with_invalid_models_raises_error(self):
        with patch('builtins.input', return_value='') as _:
            test_folder = self.get_test_folder()

            with self.assertRaises(InvalidModelError) as context:
                create_all(test_folder, ['u', 'v', 's'], models=['InvalidModel', 'DogModel', 'InvalidModel2',])

            self.assertEqual('InvalidModelError: InvalidModel, InvalidModel2 not found on models.py', str(context.exception))
            self.assertFalse(os.path.exists(os.path.join(test_folder, 'serializers.py')))
            self.assertFalse(os.path.exists(os.path.join(test_folder, 'views.py')))
            self.assertFalse(os.path.exists(os.path.join(test_folder, 'urls.py')))

    def test_create_all_appends_new_serializers_if_serializers_file_exists(self):
        test_folder = self.get_test_folder()
        with open(os.path.join(test_folder, 'expected_files/', 'serializers-expected-specific-models.py'), 'r') as existing_serializer:
            with open(os.path.join(test_folder, 'serializers.py'), 'w') as existing_file:
                existing_file.write(existing_serializer.read())
        
        with patch('builtins.input', return_value='y') as _:

            create_all(test_folder, ['s'], models=["EventModel"])

        self.assertFile(test_folder, 'serializers-expected-append.py', 'serializers.py')

    def test_create_all_appends_new_views_if_views_file_exists(self):
        test_folder = self.get_test_folder()
        with open(os.path.join(test_folder, 'expected_files/', 'views-expected-specific-models.py'), 'r') as existing_views:
            with open(os.path.join(test_folder, 'views.py'), 'w') as existing_file:
                existing_file.write(existing_views.read())
        
        with patch('builtins.input', return_value='y') as _:
            create_all(test_folder, ['v'], models=["EventModel"])

        self.assertFile(test_folder, 'views-expected-append.py', 'views.py')

    def test_create_all_appends_new_urls_if_urls_file_exists(self):
        test_folder = self.get_test_folder()
        with open(os.path.join(test_folder, 'expected_files/', 'urls-expected-specific-models.py'), 'r') as existing_urls:
            with open(os.path.join(test_folder, 'urls.py'), 'w') as existing_file:
                existing_file.write(existing_urls.read())
        
        with patch('builtins.input', return_value='y') as _:
            create_all(test_folder, ['u'], models=["EventModel"])

        self.assertFile(test_folder, 'urls-expected-append.py', 'urls.py')


class CommandLineTest(FileTestMixin, unittest.TestCase):
    def test_command_line_override_false_do_not_create_files(self):
        test_folder = self.get_test_folder()
        with patch('builtins.input', return_value='n') as _:
            create_all(test_folder, ['v', 's', 'u'])
            for file in FILES:
                self.assertFalse(os.path.exists(os.path.join(test_folder, file)))

    def test_command_line_override_force_true_create_files_without_prompt(self):
        test_folder = self.get_test_folder()
        create_all(test_folder, ['v', 's', 'u'], force=True)
        for file in FILES:
            self.assertTrue(os.path.exists(os.path.join(test_folder, file)))


if __name__ == '__main__':
    unittest.main()