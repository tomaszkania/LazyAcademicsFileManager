import os
import filecmp
from utils.ext_manager import Extensions


class Duplicates(Extensions):
    """
    A class to find and remove duplicate files in a specified directory.

    The `Duplicates` class inherits from the `Extensions` class and provides functionality
    to identify duplicate files in a directory, list them, and remove them.

    Methods:
        find_duplicates() -> List[List[str]]:
            Finds and returns a list of duplicate files grouped in lists.
        display_duplicates() -> None:
            Displays the duplicate files found in the directory.
        remove_duplicates() -> None:
            Removes duplicate files found in the directory.

    Usage:
        To use this class, instantiate a `Duplicates` object with a path to the directory you want to check
        for duplicate files. Call the `find_duplicates` method to find the duplicate files, or use the
        `display_duplicates` method to display them. To remove the duplicate files, call the `remove_duplicates` method.

        Example:
            duplicates = Duplicates("path/to/your/directory")
            duplicate_files = duplicates.find_duplicates()
            duplicates.display_duplicates()
            duplicates.remove_duplicates()
    """

    def __init__(self, path: str):
        super().__init__(path)

    def find_duplicates(self) -> List[List[str]]:
        files = sorted(self.files)
        duplicates = []
        for f in files:
            is_duplicate = False
            for equivalence_class in duplicates:
                is_duplicate = filecmp.cmp(
                    os.path.join(self.path, f),
                    os.path.join(self.path, equivalence_class[0]),
                    shallow=True
                )
                if is_duplicate:
                    equivalence_class.append(f)
                    break
            if not is_duplicate:
                duplicates.append([f])
        return [dup_group for dup_group in duplicates if len(dup_group) > 1]

    def display_duplicates(self) -> None:
        duplicate_groups = self.find_duplicates()
        if not duplicate_groups:
            print("No duplicate files found!")
        else:
            print("Duplicated files:")
            for group in duplicate_groups:
                print(", ".join(group))

    def remove_duplicates(self) -> None:
        duplicate_groups = self.find_duplicates()
        files_removed = 0
        for group in duplicate_groups:
            for f in group[1:]:
                os.remove(os.path.join(self.path, f))
                files_removed += 1
        print(f"{files_removed} duplicate files removed!")
