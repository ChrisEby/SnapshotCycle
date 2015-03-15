# __author__ = 'Chris Eby'

from configparser import ConfigParser
from os import path
from subprocess import Popen, PIPE
import shlex


def main():
    config_file = 'settings.ini'

    # Check if the ini file exists, create if not
    if not path.isfile(config_file):
        create_ini(config_file)
        print(config_file, ' not found, a default one has been created.  Set it up and then re-run.')
        quit()

    # Read in all the settings
    config = ConfigParser()
    config.read(config_file)
    backup_root = config.get('cycle', 'backup_root')
    directories = config.get('cycle', 'directories').split()
    dir_prefix = config.get('cycle', 'dir_prefix')
    max_backups = config.getint('cycle', 'max_backups')
    debug = config.getboolean('cycle', 'debug')

    # Drop out one from the # of backups
    max_backups -= 1

    for directory in directories:
        print('Working folder: ' + directory)

        directory = backup_root + directory

        last_backup = directory + dir_prefix + str('%02d' % max_backups)
        print('Removing last backup')
        run_cmd('rm -R ' + last_backup, debug)

        # Loop through the snapshots and move each backup by one in the chain
        print('Moving target folders')
        for x in range(max_backups, 0, -1):
            src_index = x - 1
            dest = directory + dir_prefix + ('%02d' % x)
            src = directory + dir_prefix + ('%02d' % src_index)
            run_cmd('mv ' + src + ' ' + dest, debug)

        print('Hard linking first snapshot to current snapshot')
        run_cmd('cp -al ' + directory + dir_prefix + '01 ' + directory + dir_prefix + '00', debug)


def run_cmd(cmd, debug):
    if debug:
        print(cmd)
        return

    process = Popen(shlex.split(cmd), stdout=PIPE)
    dump_output = process.communicate()[0]
    exit_code = process.wait()
    if exit_code != 0:
        print(dump_output)
        raise Exception(str(exit_code) + ' - Error executing command.  Please review output.')


def create_ini(config_file):
    config = ConfigParser()
    config['cycle'] = {
        'backup_root': '/path/to/backups/',
        'directories': 'dir1 dir2 dir3',
        'dir_prefix': 'daily.',
        'max_backups': 15,
        'debug': True
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    main()