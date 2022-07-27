import os
import filecmp
from utils.ext_manager import Extensions


class Duplicates(Extensions):

    def __init__(self, path):
        super().__init__(path)

    def remove_duplicated_files(self):
        files = sorted(self.files)
        duplicated = []
        for f in files:
            is_dupl = False
            for equivalence_class in duplicated:
                is_dupl = filecmp.cmp(
                    os.path.join(self.path, f),
                    os.path.join(self.path, equivalence_class[0]),
                    shallow=True
                )
                if is_dupl:
                    equivalence_class.append(f)
                    os.remove(os.path.join(self.path, f))
                    break
            if not is_dupl:
                duplicated.append([f])
        print(f"{len(files) - len(duplicated)} duplicated files removed!")
