import argparse
import datetime
from virtual_fs import VirtualFileSystem

class ShellEmulator:
    def __init__(self, hostname, zip_path):
        self.hostname = hostname
        self.vfs = VirtualFileSystem(zip_path)

    def run(self):
        while True:
            command = input(f"{self.hostname}: $ ")
            if command in ['exit', 'quit']:
                break
            elif command == 'ls':
                files = self.vfs.list_files()
                print('\n'.join(files))
            elif command.startswith('cat '):
                filename = command[4:]  # Получаем имя файла
                content = self.vfs.read_file(filename)
                print(content.decode() if isinstance(content, bytes) else content)
            elif command == 'cal':
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            elif command == 'head':
                print("head command is not implemented yet.")
            else:
                print("Command not found.")

def main():
    parser = argparse.ArgumentParser(description='Shell Emulator')
    parser.add_argument('hostname', help='Hostname displayed in prompt')
    parser.add_argument('zip_path', help='Path to the virtual file system ZIP archive')
    args = parser.parse_args()

    emulator = ShellEmulator(args.hostname, args.zip_path)
    emulator.run()

if __name__ == "__main__":
    main()