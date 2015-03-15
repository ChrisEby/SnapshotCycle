Snapshot Cycle
====================

#### Overview

Uses hardlinks to cycle snapshots (folders) on a Linux system.  Useful for scenarios where you want to take a backup over a recurring time period (hourly, daily, etc) and not take up as much space on the target system. 

#### Compatibility

Python 3.4+

#### Getting Started

Just run it first and it will generate a stock settings file.  From there it will exit and you can set up the settings.ini file with your information.  Then just re-run it and it will do its thing.

```
[DEFAULT]
backup_root = /path/to/backups/
directories = dir1 dir2 dir3
dir_prefix = daily.
max_backups = 15
debug = True
```

#### Caveats

Make sure the user running the script has permission to the backup_root specified.

Setting the debug flag to true will print the commands to be run instead of running them.

Enjoy!