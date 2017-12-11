class bcol:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

_H_DETECT = "[" + bcol.GREEN + "-DETECT-" + bcol.ENDC + "] "
_H_MAIN = "[" + bcol.WARNING + "-MAIN-" + bcol.ENDC + "] "
_H_AUDIO = "[" + bcol.GREEN + "-AUDIO-" + bcol.ENDC + "] "
_H_CAPTURE = "[" + bcol.GREEN + "-CAPTURE-" + bcol.ENDC + "] "
_H_SONAR = "[" + bcol.GREEN + "-SONAR-" + bcol.ENDC + "] "