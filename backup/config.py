import yaml


class Config:
    def __init__(self, config_file):
        self._config_file = config_file
        self._config = self._read_config_file(self._config_file)

    def aws_profile(self) -> str:
        return self._config['aws_profile']

    def kms_key(self) -> str:
        return self._config['kms_key']

    def encryption_context(self) -> str:
        return self._config['encryption_context']

    def s3_bucket(self) -> str:
        return self._config['s3_bucket']

    def intermediate_path(self) -> str:
        return self._config.get('intermediate_path', '/tmp/')

    def backup_paths(self) -> list:
        return [(path_info['title'], path_info['path'], path_info.get('ignore', [])) for path_info in
                self._config['backup']]

    @staticmethod
    def _read_config_file(file_path) -> dict:
        with open(file_path) as config_file:
            return yaml.safe_load(config_file)
