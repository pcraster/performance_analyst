version_major       = 0
version_minor       = 0
version_patch_level = 10


def version_as_integer():
    """
    Return version as an integer: <major> * 100 + <minor> * 10 + <patch>
    """
    return version_major * 100 + version_minor * 10 + version_patch_level


def version_as_string():
    """
    Return version as a string: <major>.<minor>.<patch>
    """
    return "{}.{}.{}".format(version_major, version_minor, version_patch_level)


def version_as_tuple():
    """
    Return version as a tuple: (<major>, <minor>, <patch>)
    """
    return (version_major, version_minor, version_patch_level)
