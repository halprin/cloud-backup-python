from backup.compressfile import CompressFile
from backup.encryptedfile import EncryptedFile
import os


class BackupFile:
    def __init__(self, title, path_to_backup, ignores=None):
        self.title = title
        self.path = path_to_backup
        self.saved_encrypted_path = None
        self.ignores = ignores

    def archive(self, kms_key, aws_profile):
        print('Compressing {}...'.format(self.title))
        compressed_file = CompressFile(self.path, '/tmp/{}.tgz'.format(self.title), ignores=self.ignores)
        compressed_file.compress()

        print('Encrypting {}...'.format(self.title))
        encrypted_file = EncryptedFile(compressed_file.compressed_path(), '/tmp/{}.cipher'.format(self.title), kms_key,
                                       aws_profile)
        encrypted_file.encrypt()

        os.remove(compressed_file.compressed_path())
        self.saved_encrypted_path = encrypted_file.encrypted_path()

        print('Completed {}...'.format(self.title))

    def archived_path(self):
        return self.saved_encrypted_path

    def cleanup(self):
        os.remove(self.saved_encrypted_path)
