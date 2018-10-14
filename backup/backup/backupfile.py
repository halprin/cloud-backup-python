from .compression.compressfile import CompressFile
from .encryption.encryptedfile import EncryptedFile
import os


class BackupFile:
    def __init__(self, title, path_to_backup, ignores=None, intermediate_path='/tmp/'):
        self.title = title
        self.path = path_to_backup
        self.saved_encrypted_path = None
        self.ignores = ignores
        self.intermediate_path = intermediate_path if intermediate_path is not None else '/tmp/'

    def archive(self, kms_key, aws_profile, encryption_context=None):
        print('Compressing {}...'.format(self.title))
        compressed_file = CompressFile(self.path, '{}/{}.tgz'.format(self.intermediate_path, self.title),
                                       ignores=self.ignores)
        compressed_file.compress()

        print('Encrypting {}...'.format(self.title))
        encrypted_file = EncryptedFile(compressed_file.compressed_path(),
                                       '{}/{}.cipher'.format(self.intermediate_path, self.title), kms_key, aws_profile,
                                       encryption_context=encryption_context)
        encrypted_file.encrypt()

        os.remove(compressed_file.compressed_path())
        self.saved_encrypted_path = encrypted_file.encrypted_path()

        print('Completed {}...'.format(self.title))

    def archived_path(self):
        return self.saved_encrypted_path

    def cleanup(self):
        os.remove(self.saved_encrypted_path)
