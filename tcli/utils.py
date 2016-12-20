import os
import re
import itertools
from stat import S_IMODE, S_ISREG, ST_MODE


def is_executable_posix(path):
    """Whether the file is executable.
    Based on which.py from stdlib
    """

    try:
        st = os.stat(path)
    except os.error:
        return None

    isregfile = S_ISREG(st[ST_MODE])
    isexemode = (S_IMODE(st[ST_MODE]) & 0111)
    return bool(isregfile and isexemode)


def canonical_path(path):
    return os.path.realpath(os.path.normcase(path))


def find_plugin_executables(pattern):
    filepred = re.compile(pattern).search
    filter_files = lambda files: itertools.ifilter(filepred, files)
    is_executable = is_executable_posix

    seen = set()
    plugins = []
    for dirpath in os.environ.get('PATH', '').split(os.pathsep):
        if os.path.isdir(dirpath):
            rp = canonical_path(dirpath)
            if rp in seen:
                continue
            seen.add(rp)

            for filename in filter_files(os.listdir(dirpath)):
                path = os.path.join(dirpath, filename)
                isexe = is_executable(path)

                if isexe:
                    cmd = os.path.basename(path)
                    name = re.search(pattern, cmd).group(1)
                    plugins.append((name, cmd))
    return plugins
