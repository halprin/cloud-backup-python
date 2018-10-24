import os
import tarfile
from ...cli import cli_library


class CompressFile:
    def __init__(self, path_to_compress, out_path, ignores=None):
        self.path = path_to_compress
        self.out_path = out_path
        self.ignores = ignores

    def compress(self):
        with tarfile.open(self.out_path, mode='w:gz') as tar_file:
            for root, directories, files in os.walk(self.path):
                if self._exclude_filter(root):
                    continue
                for file in files:
                    full_path = os.path.join(root, file)
                    if self._exclude_filter(full_path):
                        continue
                    try:
                        tar_file.add(full_path, os.path.relpath(full_path, os.path.join(self.path, '..')),
                                     recursive=False)
                    except OSError:
                        cli_library.echo("Couldn't write {}".format(full_path))
                        pass

    def compressed_path(self):
        return self.out_path

    def _exclude_filter(self, filename):
        exclude = False

        for ignore in self.ignores:
            if filename.find(ignore) != -1:
                exclude = True
                break

        return exclude
