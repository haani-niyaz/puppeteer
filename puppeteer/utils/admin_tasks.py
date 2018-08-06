
"""System admin tasks"""

import os
import errno
import pwd
from shutil import copyfile


class AdminTasksError(Exception):
    """An exception that occurs when performing administrative operations"""
    pass


def make_dirs(dirs):
    """Create directories recursively"""

    try:
        os.makedirs(dirs)
    except OSError, e:
        if e.errno == errno.EEXIST:
            return ("'%s' Directory already exists" % dirs)
        else:
            raise AdminTasksError(
                "Backup directory creation failed with error %s" % str(e))