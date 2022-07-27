import os
import shutil
from typing import List


class Extensions:

    DOCS = "Documents"
    APPS = "Executables"
    MISC = "Misc"
    ARCH = "Archives"
    PICS = "Pictures"

    document_extensions: List[str] = ["pdf", "docx", "djvi", "doc"]
    pictures_extensions: List[str] = ["png", "jpg", "jpeg", "gif", "djvu"]
    archives_extensions: List[str] = [
        "zip",
        "rar",
        "gz",
        "tar",
        "iso",
        "7z",
        "deb"
        ]
    executab_extensions: List[str] = ["exe", "bat"]

    assignment_dictionary = {
        DOCS: document_extensions,
        APPS: executab_extensions,
        ARCH: archives_extensions,
        PICS: pictures_extensions,
    }

    reserved_extensions = sum(assignment_dictionary.values(), [])

    def __init__(self, path):
        self.path = path
        self.files = self.get_files(path)

    @staticmethod
    def extension(string: str) -> str:
        if type(string) != str:
            raise Exception("The input is not a string.")
        else:
            position = string.rfind('.')
            ext = string[position + 1:]
        return ext

    def get_extension(self, path: str) -> List[str]:
        files = []
        for entry in os.scandir(path):
            if entry.is_file():
                files.append(self.extension(entry.name))
        return list(set(files))

    @staticmethod
    def get_files(path: str) -> List[str]:
        files = []
        for entry in os.scandir(path):
            if entry.is_file():
                files.append(entry.name)
            else:
                continue
        return files

    def segregate(self, path: str) -> None:
        extensns = self.get_extension(path)
        for ext in extensns:
            if ext in self.reserved_extensions:
                for key in self.assignment_dictionary.keys():
                    if ext in self.assignment_dictionary[key]:
                        destpath = os.path.join(path, key)
                        os.makedirs(destpath, exist_ok=True)
            else:
                destpath = os.path.join(path, "Misc", ext)
                os.makedirs(destpath, exist_ok=True)

    def moving(self, key: str, f: str, ext: str) -> None:
        nfile = os.path.join(self.path, key, f)
        if os.path.exists(nfile):
            dictfiles = {}
            i, temp = 1, f
            position = f.rfind('.')
            # geting the file name before .extension
            file_name = f[0: position]
            while os.path.exists(
                os.path.join(self.path, key, temp)
            ):
                temp = os.path.join(self.path, key, f"{file_name}_{i}.{ext}")
                dictfiles[file_name] = temp
                i += 1
            shutil.move(
                os.path.join(self.path, f),
                os.path.join(self.path, key, temp)
            )
        else:
            shutil.move(
                os.path.join(self.path, f),
                os.path.join(self.path, key, f)
            )

    def group_by_extension(self):
        self.segregate(self.path)
        for f in self.files:
            ext = self.extension(f)
            if ext in self.reserved_extensions:
                for key, value in self.assignment_dictionary.items():
                    if ext in value:
                        self.moving(key, f, ext)
            else:
                nfile = os.path.join(self.path, "Misc", ext, f)
                shutil.move(os.path.join(self.path, f), nfile)
