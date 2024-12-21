import unittest
import zipfile
import os
from virtual_fs import VirtualFileSystem


class TestVirtualFileSystem(unittest.TestCase):
    def setUp(self):
        # Создание временного zip-файла для тестирования
        self.zip_path = 'test.zip'
        with zipfile.ZipFile(self.zip_path, 'w') as z:
            z.writestr('file1.txt', 'content of file 1')
            z.writestr('file2.txt', 'content of file 2')

        self.vfs = VirtualFileSystem(self.zip_path)

    def test_list_files(self):
        files = self.vfs.list_files()
        self.assertIn('file1.txt', files)
        self.assertIn('file2.txt', files)

    def test_read_file(self):
        content = self.vfs.read_file('file1.txt')
        self.assertEqual(content, b'content of file 1')

    def tearDown(self):
        os.remove(self.zip_path)


if __name__ == "__main__":
    unittest.main()