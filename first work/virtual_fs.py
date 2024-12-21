import zipfile
from pathlib import Path

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.files = {}

        with zipfile.ZipFile(zip_path) as z:
            for name in z.namelist():
                self.files[name] = z.read(name)

    def list_files(self):
        return list(self.files.keys())

    def read_file(self, filename):
        return self.files.get(filename, b'File not found')