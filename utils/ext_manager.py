import os
import shutil
from typing import List, Dict


class Extensions:
    """
    A class designed to organise files within a given directory based on their file extensions.

    The `Extensions` class provides functionality to segregate files into different categories,
    such as Documents, Executables, Archives, Pictures, and Miscellaneous, based on their file
    extensions. The class creates subdirectories for each category and moves the files into
    their respective subdirectories.

    Attributes:
        DOCS (str): A string representing the "Documents" category.
        APPS (str): A string representing the "Executables" category.
        MISC (str): A string representing the "Miscellaneous" category.
        ARCH (str): A string representing the "Archives" category.
        PICS (str): A string representing the "Pictures" category.

        document_extensions (List[str]): A list of file extensions belonging to the "Documents" category.
        pictures_extensions (List[str]): A list of file extensions belonging to the "Pictures" category.
        archives_extensions (List[str]): A list of file extensions belonging to the "Archives" category.
        executab_extensions (List[str]): A list of file extensions belonging to the "Executables" category.

        assignment_dictionary (Dict[str, List[str]]): A dictionary mapping category names to their respective file extensions.
        reserved_extensions (List[str]): A list of all reserved file extensions.

    Methods:
        extension(string: str) -> str:
            Returns the file extension of a given filename.
        get_extension(path: str) -> List[str]:
            Returns a list of unique file extensions in the specified directory.
        get_files(path: str) -> List[str]:
            Returns a list of file names in the specified directory.
        segregate(path: str) -> None:
            Creates subdirectories for each category based on file extensions.
        moving(key: str, f: str, ext: str) -> None:
            Moves a file to the appropriate subdirectory based on its extension.
        group_by_extension():
            Organises files in the directory by grouping them into subdirectories based on their extensions.

    Usage:
        To use this class, instantiate an `Extensions` object with the path to the directory containing
        the files you wish to organise. Then, call the `group_by_extension()` method to organise the files
        into their respective subdirectories based on their file extensions.

        Example:
            directory_path = "path/to/your/directory"
            ext = Extensions(directory_path)
            ext.group_by_extension()
    """


    DOCS = "Documents"
    APPS = "Executables"
    MISC = "Misc"
    ARCH = "Archives"
    PICS = "Pictures"

    document_extensions: List[str] = [
        "pdf",
        "docx",
        "djvi",
        "doc",
        "txt",
        "tex",
        "rtf",
        "odt",
        "wpd",
        "wps",
        "ods",
    ]
    pictures_extensions: List[str] = [
        "png",
        "jpg",
        "jpeg",
        "gif",
        "djvu",
        "tif",
        "tiff",
        "bmp",
        "svg",
        "eps",
    ]
    archives_extensions: List[str] = [
        "zip",
        "rar",
        "gz",
        "tar",
        "iso",
        "7z",
        "deb",
        "pkg",
        "rpm",
        "xz",
        "tgz",
    ]
    executab_extensions: List[str] = [
        "exe",
        "bat",
        "sh",
        "msi",
        "bin",
        "jar",
        "app",
        "apk",
        "run",
        "com",
        "gadget",
    ]

    assignment_dictionary = {
        DOCS: document_extensions,
        APPS: executab_extensions,
        ARCH: archives_extensions,
        PICS: pictures_extensions,
    }

    reserved_extensions = sum(assignment_dictionary.values(), [])

    def __init__(self, path: str):
        """
        Initialise an `Extensions' instance.

        Parameters:
            path (str): The directory path containing the files.
        """
        self.path = path
        self.files = self.get_files(path)

    @staticmethod
    def extension(string: str) -> str:
        """
        Get the extension of a given filename.

        Parameters:
            string (str): The filename.

        Returns:
            str: The file extension.
        """
        if type(string) != str:
            raise Exception("The input is not a string.")
        else:
            position = string.rfind(".")
            ext = string[position + 1 :]
        return ext

    def get_extension(self, path: str) -> List[str]:
        """
        Get a list of unique file extensions in the directory.

        Parameters:
            path (str): The directory path.

        Returns:
            List[str]: A list of unique file extensions.
        """
        files = []
        for entry in os.scandir(path):
            if entry.is_file():
                files.append(self.extension(entry.name))
        return list(set(files))

    @staticmethod
    def get_files(path: str) -> List[str]:
        """
        Get a list of file names in the directory.

        Parameters:
            path (str): The directory path.

        Returns:
            List[str]: A list of file names.
        """
        files = []
        for entry in os.scandir(path):
            if entry.is_file():
                files.append(entry.name)
            else:
                continue
        return files

    def segregate(self, path: str) -> None:
        """
        Create subdirectories for each category based on file extensions.

        Parameters:
            path (str): The directory path.
        """
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
        """
        Move a file to the appropriate subdirectory based on its extension.

        Parameters:
            key (str): the category name.
            f (str): the file name.
            ext (str): the file extension.    
        """
        nfile = os.path.join(self.path, key, f)
        if os.path.exists(nfile):
            dictfiles = {}
            i, temp = 1, f
            position = f.rfind(".")
            # geting the file name before .extension
            file_name = f[0:position]
            while os.path.exists(os.path.join(self.path, key, temp)):
                temp = os.path.join(self.path, key, f"{file_name}_{i}.{ext}")
                dictfiles[file_name] = temp
                i += 1
            shutil.move(os.path.join(self.path, f), os.path.join(self.path, key, temp))
        else:
            shutil.move(os.path.join(self.path, f), os.path.join(self.path, key, f))

    def group_by_extension(self):
        """
        Organise files in the directory by grouping them into subdirectories
        based on their extensions.
        """
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


if __name__ == "__main__":
    directory_path = r"D:\Archived_downloads"
    ext = Extensions(directory_path)
    ext.group_by_extension()
