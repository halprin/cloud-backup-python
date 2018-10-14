import click
from ..config import Config
from ..backup.backupset import BackupSet


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
def restore(config_file):
    click.echo('Initiating restore using {}'.format(config_file))

    config = Config(config_file)

    click.echo('Completed restore')
