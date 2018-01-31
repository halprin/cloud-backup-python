from backup.backupset import BackupSet
import yaml


def read_config_file(path):
    with open(path) as config_file:
        return yaml.safe_load(config_file)


if __name__ == '__main__':

    config = read_config_file('backup.yml')

    aws_profile = config['aws_profile']
    kms_key = config['kms_key']
    s3_bucket = config['s3_bucket']
    intermediate_path = config.get('intermediate_path', '/tmp/')
    backup_paths = [(path_info['title'], path_info['path'], path_info.get('ignore', [])) for path_info in
                    config['backup']]

    backup_set = BackupSet(backup_paths, s3_bucket, kms_key, aws_profile, intermediate_path)
    backup_set.backup()
