from .config import Config
from boto3.session import Session
from .cli import cli_library
from os import path


def list_timestamps(config: Config):
    s3_client = Session(profile_name=config.aws_profile()).client('s3')
    object_listing = s3_client.list_objects(Bucket=config.s3_bucket(), Delimiter='/')

    prefixes = object_listing.get('CommonPrefixes')
    if prefixes is None:
        cli_library.echo('No backup timestamps')
        return

    for prefix in prefixes:
        prefix_sans_slash = prefix.get('Prefix')[0:-1]
        cli_library.echo('* {}'.format(prefix_sans_slash))


def list_backup_files(config: Config, timestamp: str):
    s3_resource = Session(profile_name=config.aws_profile()).resource('s3')
    backup_bucket = s3_resource.Bucket(config.s3_bucket())

    for s3_object in backup_bucket.objects.filter(Prefix=timestamp):
        base_filename = path.splitext(path.basename(s3_object.key))[0]
        cli_library.echo('* {}'.format(base_filename))
