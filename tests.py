import os
import zipfile
import unittest
from emulator import VirtualFileSystem


class TestVirtualFileSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.zip_path = 'test.zip'
        with zipfile.ZipFile(cls.zip_path, 'w') as z:
            z.writestr('file1.txt', 'Hello, World!')
            z.writestr('file2.txt', 'This is a test file.')
            z.writestr('subdir/file3.txt', 'Another file in a subdirectory.')

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.zip_path)

    def setUp(self):
        self.vfs = VirtualFileSystem(self.zip_path)

    def test_ls(self):
        expected_files = ['file1.txt', 'file2.txt', 'subdir']
        self.assertEqual(sorted(self.vfs.ls()), sorted(expected_files))

    def test_cd(self):
        self.vfs.cd('subdir')
        self.assertEqual(self.vfs.current_path, '/subdir')

    def test_uptime(self):
        uptime = self.vfs.uptime()
        self.assertGreaterEqual(uptime, 0)

    def test_whoami(self):
        username = 'testuser'
        self.assertEqual(self.vfs.whoami(username), username)

    def test_invalid_cd(self):
        self.vfs.cd('nonexistent')
        self.assertEqual(self.vfs.current_path, '/')

    def test_cd_parent_directory(self):
        self.vfs.cd('subdir')
        self.vfs.cd('..')
        self.assertEqual(self.vfs.current_path, '/')


if __name__ == "__main__":
    unittest.main()
