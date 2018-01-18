from backup.backupset import BackupSet
import yaml


if __name__ == '__main__':

    config = {}
    with open('backup.yml') as config_file:
        config = yaml.safe_load(config_file)

    aws_profile = config['aws_profile']
    kms_key = config['kms_key']
    s3_bucket = config['s3_bucket']
    backup_paths = [(path_info['title'], path_info['path'], path_info.get('ignore', [])) for path_info in
                    config['backup']]

    backup_set = BackupSet(backup_paths, s3_bucket, kms_key, aws_profile)
    backup_set.backup()
