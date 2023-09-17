def error(msg: str) -> None:
    print('\033[1;31m[ERROR]: ' + msg + '\033[0m')


def fatal(msg: str) -> None:
    print('\033[1;31m[FATAL]: ' + msg + '\033[0m')
    exit()


def warning(msg: str) -> None:
    print('\033[1;33m[WARNING]: ' + msg + '\033[0m')
