import os
import tarfile


class CompressFile:
    def __init__(self, path_to_compress, out_path, ignores=None):
        self.path = path_to_compress
        self.out_path = out_path
        self.ignores = ignores

    def compress(self):
        with tarfile.open(self.out_path, mode='w:gz') as tar_file:
            tar_file.add(self.path, os.path.relpath(self.path, os.path.join(self.path, '..')),
                         exclude=self._exclude_filter)

    def compressed_path(self):
        return self.out_path

    def _exclude_filter(self, filename):
        exclude = False

        for ignore in self.ignores:
            if filename.find(ignore) != -1:
                exclude = True
                break

        return exclude
