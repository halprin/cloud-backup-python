from boto3 import Session
from boto3.s3.transfer import S3Transfer
from .compression.uncompressfile import UncompressFile
from .encryption.decryptedfile import DecryptedFile
import os
import click


class RestoreFile:
    def __init__(self, s3_bucket, timestamp, backup_file, restore_path, intermediate_path='/tmp/'):
        self.s3_bucket = s3_bucket
        self.timestamp = timestamp
        self.backup_file = backup_file
        self.restore_path = restore_path
        self.intermediate_path = intermediate_path if intermediate_path is not None else '/tmp/'

    def restore(self, kms_key, aws_profile, encryption_context=None):
        self._download(aws_profile)
        self._decrypt(kms_key, aws_profile, encryption_context)
        self._uncompress()

    def restore_path(self):
        return self.saved_encrypted_path

    def cleanup(self):
        os.remove(self.saved_encrypted_path)

    def _download(self, aws_profile):
        print('Downloading {}...'.format(self.backup_file))

        s3_object = self.timestamp + '/' + self.backup_file + '.cipher'
        s3_client = Session(profile_name=aws_profile).client('s3')
        s3_object_size = s3_client.head_object(Bucket=self.s3_bucket, Key=s3_object)['ContentLength']

        self._progress_bar = click.progressbar(length=s3_object_size, label='Downloading')

        transfer_manager = S3Transfer(s3_client)
        transfer_manager.download_file(self.s3_bucket, s3_object, self._local_cipher_file(),
                                       callback=self._download_progress_callback)
        self._progress_bar.finish()
        print()

    def _decrypt(self, kms_key, aws_profile, encryption_context):
        print('Decrypting {}...'.format(self.backup_file))

        decrypted_file = DecryptedFile(self._local_cipher_file(), self._local_compress_file(), kms_key, aws_profile,
                                       encryption_context)
        decrypted_file.decrypt()

        os.remove(self._local_cipher_file())

    def _uncompress(self):
        print('Uncompressing {}...'.format(self.backup_file))

        uncompress_file = UncompressFile(self._local_compress_file(), self.restore_path)
        uncompress_file.uncompress()

        os.remove(self._local_compress_file())

    def _download_progress_callback(self, bytes_transfered):
        self._progress_bar.update(bytes_transfered)

    def _local_cipher_file(self):
        return os.path.join(self.intermediate_path, self.backup_file + '.cipher')

    def _local_compress_file(self):
        return os.path.join(self.intermediate_path, self.backup_file + '.tgz')
