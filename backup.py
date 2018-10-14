from backup.backupset import BackupSet
import yaml
import sys

from backup.encryption.decryptedfile import DecryptedFile


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
    encryption_context = config['encryption_context']
    s3_bucket = config['s3_bucket']
    intermediate_path = config.get('intermediate_path', '/tmp/')
    backup_paths = [(path_info['title'], path_info['path'], path_info.get('ignore', [])) for path_info in
                    config['backup']]

    decrypted_file = DecryptedFile('/Volumes/Backup/Archive/Cloud/peter_music.cipher',
                                   '/Volumes/Backup/Archive/Cloud/peter_music.tgz', kms_key, aws_profile,
                                   encryption_context=encryption_context)

    decrypted_file.decrypt()
    # backup_set = BackupSet(backup_paths, s3_bucket, kms_key, encryption_context, aws_profile, intermediate_path)
    # backup_set.backup()
