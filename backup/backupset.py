from boto3 import Session
from boto3.s3.transfer import S3Transfer
import os
from datetime import datetime, timezone
from concurrent.futures import ProcessPoolExecutor
from concurrent import futures
from backup.backupfile import BackupFile


class BackupSet:
    def __init__(self, paths, s3_bucket, kms_key, aws_profile, intermediate_path):
        self.paths = paths
        self.s3_bucket = s3_bucket
        self.kms_key = kms_key
        self.aws_profile = aws_profile
        self.intermediate_path = intermediate_path

    def backup(self):
        future_set = self._archive()
        futures.wait(future_set)

        archived_paths = [future.result() for future in future_set]
        self._upload(archived_paths)

        print('Uploads complete')

        self._cleanup(archived_paths)
        print('Done')

    def _archive(self):
        future_set = set()

        with ProcessPoolExecutor() as executor:
            for current_title, current_path, current_ignores in self.paths:
                current_backup_file = BackupFile(current_title, current_path, ignores=current_ignores,
                                                 intermediate_path=self.intermediate_path)
                future_set.add(executor.submit(self._archive_backup_file, current_backup_file))

        return future_set

    def _archive_backup_file(self, backup_file):
        backup_file.archive(self.kms_key, self.aws_profile)
        return backup_file.archived_path()

    def _upload(self, archive_paths):
        transfer_manager = S3Transfer(Session(profile_name=self.aws_profile).client('s3'))

        date_time = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
        print('Uploading {} backup set...'.format(date_time))

        for current_path in archive_paths:
            current_basename = os.path.basename(current_path)
            transfer_manager.upload_file(current_path, self.s3_bucket, '{}/{}'.format(date_time, current_basename))

    @staticmethod
    def _cleanup(archived_paths):
        print('Cleaning up...')
        for archive_path in archived_paths:
            os.remove(archive_path)
