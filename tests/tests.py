import unittest
import os
from unittest.mock import patch
from django_easy_drf.main import create_all, create_serializers, create_views, create_urls


FILES = ['serializers.py', 'views.py', 'urls.py']

class FileTestMixin:
    def _assertFile(self, folder, expected_path, actual_path):
        with open(os.path.join(folder, expected_path), 'r') as expected_file:
            with open(os.path.join(folder, actual_path), 'r') as actual_file:
                self.assertEqual(expected_file.read(), actual_file.read())

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

            create_all(test_folder)

            self._assertFile(test_folder, 'serializers-expected.py', 'serializers.py')

    def test_create_all_creates_views_file_correctly(self):
        with patch('builtins.input', return_value='Y') as _:
            test_folder = self.get_test_folder()

            create_all(test_folder)

            self._assertFile(test_folder, 'views-expected.py', 'views.py')

    def test_create_all_creates_urls_file_correctly(self):
        with patch('builtins.input', return_value='') as _:
            test_folder = self.get_test_folder()

            create_all(test_folder)

            self._assertFile(test_folder, 'urls-expected.py', 'urls.py')


class CreateSerializerFileTest(FileTestMixin, unittest.TestCase):
    def test_create_serializers_creates_serializers_file_correctly(self):
        test_folder = self.get_test_folder()

        create_serializers(test_folder)

        self._assertFile(test_folder, 'serializers-expected.py', 'serializers.py')


class CreateViewsFileTest(FileTestMixin, unittest.TestCase):
    def test_create_views_creates_views_file_correctly(self):
        test_folder = self.get_test_folder()

        create_views(test_folder)

        self._assertFile(test_folder, 'views-expected.py', 'views.py')


class CreateUrlsFileTest(FileTestMixin, unittest.TestCase):
    def test_create_urls_creates_urls_file_correctly(self):
        test_folder = self.get_test_folder()

        create_urls(test_folder)

        self._assertFile(test_folder, 'urls-expected.py', 'urls.py')


class CommandLineTest(FileTestMixin, unittest.TestCase):
    def test_command_line_override_false_do_not_create_files(self):
        test_folder = self.get_test_folder()
        with patch('builtins.input', return_value='n') as _:
            create_all(test_folder)
            for file in FILES:
                self.assertFalse(os.path.exists(os.path.join(test_folder, 'serializers.py')))
                self.assertFalse(os.path.exists(os.path.join(test_folder, 'views.py')))
                self.assertFalse(os.path.exists(os.path.join(test_folder, 'urls.py')))

    def test_command_line_override_force_true_create_files_without_prompt(self):
        test_folder = self.get_test_folder()
        create_all(test_folder, force=True)
        for file in FILES:
            self.assertTrue(os.path.exists(os.path.join(test_folder, 'serializers.py')))
            self.assertTrue(os.path.exists(os.path.join(test_folder, 'views.py')))
            self.assertTrue(os.path.exists(os.path.join(test_folder, 'urls.py')))


if __name__ == '__main__':
    unittest.main()