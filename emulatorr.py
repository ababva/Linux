import os
import sys
import zipfile
import time
from pathlib import Path
import unittest

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.current_path = "/"
        self.start_time = time.time()
        self.files = {}
        self.load_virtual_fs()

    def load_virtual_fs(self):
        with zipfile.ZipFile(self.zip_path) as z:
            for file_info in z.infolist():
                normalized_path = "/" + file_info.filename.replace("\\", "/").strip("/")
                if normalized_path not in self.files:
                    if not file_info.is_dir():
                        self.files[normalized_path] = z.read(file_info.filename)
                    else:
                        self.files[normalized_path] = None

    def ls(self):
        current_path_len = len(self.current_path)
        if self.current_path != "/":
            current_path_len += 1

        current_files = [
            f[current_path_len:].split('/')[0]
            for f in self.files.keys()
            if f.startswith(self.current_path) and f != self.current_path
        ]
        return sorted(set(current_files))

    def cd(self, path):
        target_path = str(Path(self.current_path, path)).replace("\\", "/")
        if path == "..":
            if self.current_path != "/":
                self.current_path = str(Path(self.current_path).parent)
                if self.current_path == ".":
                    self.current_path = "/"
            return
        
        normalized_target_path = "/" + target_path.lstrip("/")
        if any(f.startswith(normalized_target_path + "/") for f in self.files) or normalized_target_path in self.files:
            self.current_path = normalized_target_path
        else:
            print(f"cd: no such file or directory: {path}")

    def uptime(self):
        return time.time() - self.start_time

    def whoami(self, username):
        return username

def main():
    if len(sys.argv) != 3:
        print("Usage: python emulator.py <username> <zip_path>")
        return

    username = sys.argv[1]
    zip_path = sys.argv[2]

    vfs = VirtualFileSystem(zip_path)

    try:
        while True:
            command = input(f"{username}@emulator:{vfs.current_path}$ ")
            parts = command.split()

            if not parts:
                continue

            cmd = parts[0]
            if cmd == "ls":
                print("\n".join(vfs.ls()))
            elif cmd == "cd":
                if len(parts) > 1:
                    vfs.cd(parts[1])
            elif cmd == "exit":
                print("Exiting the emulator. Goodbye!")
                break
            elif cmd == "uptime":
                print(vfs.uptime())
            elif cmd == "whoami":
                print(vfs.whoami(username))
            else:
                print(f"{cmd}: command not found")
    except KeyboardInterrupt:
        print("\nExiting the emulator. Goodbye!")

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
    if 'test' in sys.argv:
        unittest.main(argv=sys.argv[:1]) 
    else:
        main()
