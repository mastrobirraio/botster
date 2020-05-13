from logthon import Logthon


def setup_logger(module_name=__name__):
    return Logthon(module_name=module_name)
