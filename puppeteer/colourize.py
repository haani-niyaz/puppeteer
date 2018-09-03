COLORS = {'cyan': '\033[36m',
          'pink': '\033[95m',
          'blue': '\033[94m',
          'green': '\033[92m',
          'yellow': '\033[93m',
          'red': '\033[91m',
          'ENDC': '\033[0m',
          'bold': '\033[1m',
          'underline': '\033[4m'
          }


def color(color, data):
  return COLORS[color] + str(data) + COLORS['ENDC']
