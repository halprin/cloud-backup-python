import click
from ..config import Config
from ..backup.backupset import BackupSet
from ..backup.restorefile import RestoreFile
from .. import listing, installing
from .optional_int_range import OptionalIntRange
from typing import Optional
import sys


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
    try:
        restore_file.restore(config.kms_key(), config.aws_profile(), config.encryption_context())
        click.echo('Completed restore')
    except Exception as exception:
        exit_exception = click.ClickException('Restore failed!')
        exit_exception.exit_code = 3
        raise exit_exception from exception


@cli.command()
@click.argument('config_file')
@click.argument('timestamp', required=False)
def list(config_file, timestamp):
    config = Config(config_file)

    if timestamp is not None:
        click.echo('Listing backup files under {}'.format(timestamp))
        listing.list_backup_files(config, timestamp)
    else:
        click.echo('Listing backup timestamps')
        listing.list_timestamps(config)


@cli.command()
@click.argument('config_file')
@click.option('--month', prompt=True, type=OptionalIntRange(1, 12))
@click.option('--day', prompt=True, type=OptionalIntRange(1, 31))
@click.option('--weekday', prompt=True, type=OptionalIntRange(0, 7))
@click.option('--hour', prompt=True, type=OptionalIntRange(0, 23))
@click.option('--minute', prompt=True, type=OptionalIntRange(0, 59))
def install(config_file: str, month: Optional[int], day: Optional[int], weekday: Optional[int], hour: Optional[int],
            minute: Optional[int]):
    click.echo('Installing cloud backup agent')
    installing.install(sys.argv[0], config_file, month=month, day=day, weekday=weekday, hour=hour, minute=minute)
    click.echo('Completed install')


@cli.command()
def uninstall():
    click.echo('Uninstalling cloud backup agent')
    installing.uninstall()
    click.echo('Completed uninstall')


if __name__ == '__main__':
    cli()
