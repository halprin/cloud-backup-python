import click
from ..config import Config
from ..backup.backupset import BackupSet
from ..backup.restorefile import RestoreFile


@click.group()
def cli():
    pass


@cli.command()
@click.argument('config_file')
def backup(config_file):
    click.echo('Initiating back-up using {}'.format(config_file))

    config = Config(config_file)

    backup_set = BackupSet(config.backup_paths(), config.s3_bucket(), config.kms_key(), config.encryption_context(),
                           config.aws_profile(), config.intermediate_path())
    backup_set.backup()

    click.echo('Completed back-up')


@cli.command()
@click.argument('config_file')
@click.argument('timestamp')
@click.argument('backup_file')
@click.argument('restore_path', type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True,
                                                readable=False, resolve_path=True, allow_dash=False))
def restore(config_file, timestamp, backup_file, restore_path):
    click.echo('Initiating restore using {}'.format(config_file))

    config = Config(config_file)

    restore_file = RestoreFile(config.s3_bucket(), timestamp, backup_file, restore_path, config.intermediate_path())
    restore_file.restore(config.kms_key(), config.aws_profile(), config.encryption_context())

    click.echo('Completed restore')
