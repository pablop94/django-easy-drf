import unittest
import os

from django_easy_drf.main import create_all, create_serializers, create_views, create_urls


class FileTestMixin:
    def _assertFile(self, folder, expected_path, actual_path):
        with open(os.path.join(folder, expected_path), 'r') as expected_file:
            with open(os.path.join(folder, actual_path), 'r') as actual_file:
                self.assertEqual(expected_file.read(), actual_file.read())  

class CreateAllFilesTest(FileTestMixin, unittest.TestCase):

    def test_create_all_creates_serializers_file_correctly(self):
        test_folder = os.path.dirname(os.path.abspath(__file__))

        create_all(test_folder)

        self._assertFile(test_folder, 'serializers-expected.py', 'serializers.py')

    def test_create_all_creates_views_file_correctly(self):
        test_folder = os.path.dirname(os.path.abspath(__file__))

        create_all(test_folder)

        self._assertFile(test_folder, 'views-expected.py', 'views.py')

    def test_create_all_creates_urls_file_correctly(self):
        test_folder = os.path.dirname(os.path.abspath(__file__))

        create_all(test_folder)

        self._assertFile(test_folder, 'urls-expected.py', 'urls.py')


class CreateSerializerFileTest(FileTestMixin, unittest.TestCase):
    def test_create_serializers_creates_serializers_file_correctly(self):
        test_folder = os.path.dirname(os.path.abspath(__file__))

        create_serializers(test_folder)

        self._assertFile(test_folder, 'serializers-expected.py', 'serializers.py')


class CreateViewsFileTest(FileTestMixin, unittest.TestCase):
    def test_create_views_creates_views_file_correctly(self):
        test_folder = os.path.dirname(os.path.abspath(__file__))

        create_views(test_folder)

        self._assertFile(test_folder, 'views-expected.py', 'views.py')


class CreateUrlsFileTest(FileTestMixin, unittest.TestCase):
    def test_create_urls_creates_urls_file_correctly(self):
        test_folder = os.path.dirname(os.path.abspath(__file__))

        create_urls(test_folder)

        self._assertFile(test_folder, 'urls-expected.py', 'urls.py')


if __name__ == '__main__':
    unittest.main()