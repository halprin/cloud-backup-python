import os
import tarfile


class UncompressFile:
    def __init__(self, path_to_compress, out_path, ignores=None):
        self.path = path_to_compress
        self.out_path = out_path
        self.ignores = ignores

    def uncompress(self):
        pass

    def uncompressed_path(self):
        return self.out_path

    def _exclude_filter(self, filename):
        exclude = False

        for ignore in self.ignores:
            if filename.find(ignore) != -1:
                exclude = True
                break

        return exclude
