from backup.backupset import BackupSet
import yaml
import sys


def read_config_file(path):
    with open(path) as config_file:
        return yaml.safe_load(config_file)


def get_config_path():
    arguments = sys.argv
    return arguments[1] if len(arguments) > 1 else 'backup.yml'


if __name__ == '__main__':

    config_path = get_config_path()
    print('Using {} for configuration path'.format(config_path))
    config = read_config_file(config_path)

    aws_profile = config['aws_profile']
    kms_key = config['kms_key']
    s3_bucket = config['s3_bucket']
    intermediate_path = config.get('intermediate_path', '/tmp/')
    backup_paths = [(path_info['title'], path_info['path'], path_info.get('ignore', [])) for path_info in
                    config['backup']]

    backup_set = BackupSet(backup_paths, s3_bucket, kms_key, aws_profile, intermediate_path)
    backup_set.backup()
