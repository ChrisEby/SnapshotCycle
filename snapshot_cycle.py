# __author__ = 'Chris Eby'

from configparser import ConfigParser
from os import path
from subprocess import Popen, CalledProcessError, PIPE, STDOUT
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
    backup_root = config.get('DEFAULT', 'backup_root')
    directories = config.get('DEFAULT', 'directories').split()
    dir_prefix = config.get('DEFAULT', 'dir_prefix')
    max_backups = config.getint('DEFAULT', 'max_backups')
    debug = config.getboolean('DEFAULT', 'debug')

    # Drop out one from the # of backups
    max_backups -= 1

    for directory in directories:
        print('Working folder: ' + directory)

        directory = backup_root + directory + '/'
        last_backup = directory + dir_prefix + str('%02d' % max_backups)

        print('Removing last backup')
        try:
            run_cmd('rm -R ' + last_backup, debug)
        except CalledProcessError as err:
            if "No such file or directory" not in str(err.output):
                raise
            print("Last backup doesn't exist.  Skipping.")

        # Loop through the snapshots and move each backup by one in the chain
        print('Moving target folders')
        for x in range(max_backups, 0, -1):
            src_index = x - 1
            dest = directory + dir_prefix + ('%02d' % x)
            src = directory + dir_prefix + ('%02d' % src_index)
            try:
                run_cmd('mv ' + src + ' ' + dest, debug)
            except CalledProcessError as err:
                if "No such file or directory" not in str(err.output):
                    raise
                print("Cannot move directories... source doesn't exist.")

        print('Hard linking first snapshot to current snapshot')
        run_cmd('cp -al ' + directory + dir_prefix + '01 ' + directory + dir_prefix + '00', debug)


def run_cmd(cmd, debug):
    if debug:
        print(cmd)
        return
    process = Popen(shlex.split(cmd), stdout=PIPE, stderr=STDOUT)
    dump_output = process.communicate()[0]
    exit_code = process.wait()
    if exit_code != 0:
        print(dump_output)
        raise CalledProcessError(exit_code, cmd, dump_output)


def create_ini(config_file):
    config = ConfigParser()
    config['DEFAULT'] = {
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