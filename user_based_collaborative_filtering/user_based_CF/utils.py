import os

def pkg_abs_path() -> os.path:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

