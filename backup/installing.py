import os
import subprocess
from .cli import cli_library
from typing import Optional


global_daemons = '/Library/LaunchDaemons/{}'
launch_agents = '~/Library/LaunchAgents/{}'
launchd_config_path = os.path.expanduser(launch_agents).format('io.halprin.backup.plist')

template = '<?xml version="1.0" encoding="UTF-8"?> \
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"> \
<plist version="1.0"> \
    <dict> \
        <key>Label</key> \
        <string>io.halprin.backup</string> \
        <key>ProgramArguments</key> \
        <array> \
            <string>{script}</string> \
            <string>backup</string> \
            <string>{config_yml}</string> \
        </array> \
        <key>EnvironmentVariables</key> \
        <dict> \
            <key>LC_ALL</key> \
            <string>en_US.utf-8</string> \
            <key>LANG</key> \
            <string>en_US.utf-8</string> \
        </dict> \
        <key>StandardOutPath</key> \
        <string>/tmp/cloud-backup.stdout</string> \
        <key>StandardErrorPath</key> \
        <string>/tmp/cloud-backup.stderr</string> \
        <key>StartCalendarInterval</key> \
        <array> \
            <dict> \
                {interval} \
            </dict> \
        </array> \
    </dict> \
</plist>'


def install(cloud_backup_script: str, yml_config: str, month: Optional[int] = None, day: Optional[int] = None,
            weekday: Optional[int] = None, hour: Optional[int] = None, minute: Optional[int] = None):

    if os.path.exists(launchd_config_path):
        cli_library.echo('Cloud-backup agent is already installed.  Uninstalling and reinstalling.')
        uninstall()

    interval = _construct_plist_interval(month=month, day=day, weekday=weekday, hour=hour, minute=minute)
    filled = template.format(script=cloud_backup_script, config_yml=yml_config, interval=interval)

    with open(launchd_config_path, 'w') as launchd_config:
        launchd_config.write(filled)

    try:
        subprocess.run(['launchctl', 'load', launchd_config_path], check=True)
    except subprocess.CalledProcessError as exception:
        cli_library.echo(exception)
        os.remove(launchd_config_path)
        cli_library.fail_execution(4, 'Failed to load the cloud-backup agent!')


def uninstall():
    if not os.path.exists(launchd_config_path):
        cli_library.fail_execution(6, "Couldn't uninstall the cloud-backup agent because it wasn't already installed!")

    try:
        subprocess.run(['launchctl', 'unload', launchd_config_path], check=True)
    except subprocess.CalledProcessError as exception:
        cli_library.echo(exception)
        cli_library.fail_execution(5, 'Failed to unload the cloud-backup agent!')

    try:
        os.remove(launchd_config_path)
    except FileNotFoundError as exception:
        cli_library.echo(exception)
        cli_library.fail_execution(7, "Couldn't delete the cloud-backup agent!")


def _construct_plist_interval(month: Optional[int] = None, day: Optional[int] = None, weekday: Optional[int] = None,
                              hour: Optional[int] = None, minute: Optional[int] = None) -> str:
    interval = []

    if month is not None:
        interval.append('<key>Hour</key>')
        interval.append('<integer>{}</integer>'.format(month))

    if day is not None:
        interval.append('<key>Day</key>')
        interval.append('<integer>{}</integer>'.format(day))

    if weekday is not None:
        interval.append('<key>Weekday</key>')
        interval.append('<integer>{}</integer>'.format(weekday))

    if hour is not None:
        interval.append('<key>Hour</key>')
        interval.append('<integer>{}</integer>'.format(hour))

    if minute is not None:
        interval.append('<key>Minute</key>')
        interval.append('<integer>{}</integer>'.format(minute))

    return ''.join(interval)
