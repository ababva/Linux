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
                self.files[file_info.filename] = z.read(file_info.filename)

    def ls(self):
        current_files = [f for f in self.files.keys() if f.startswith(self.current_path)]
        return [f[len(self.current_path):] for f in current_files if f[len(self.current_path):].count('/') == 0]

    def cd(self, path):
        new_path = Path(self.current_path) / path
        if str(new_path).startswith('/'):
            self.current_path = str(new_path)
        else:
            self.current_path = str(Path(self.current_path) / path)

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
        # Создание временного zip файла для тестов
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
        expected_files = ['file1.txt', 'file2.txt']
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
        self.assertEqual(self.vfs.current_path, '/nonexistent')

if __name__ == "__main__":
    if 'test' in sys.argv:
        unittest.main(argv=sys.argv[:1])  #Тесты