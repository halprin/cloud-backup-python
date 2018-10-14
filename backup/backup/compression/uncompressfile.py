import os
import tarfile


class UncompressFile:
    def __init__(self, path_to_uncompress, out_path):
        self.path = path_to_uncompress
        self.out_path = out_path

    def uncompress(self):
        with tarfile.open(self.path, mode='r:gz') as tar_file:
            tar_file.extractall(path=self.out_path)

    def uncompressed_path(self):
        return self.out_path
