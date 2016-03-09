import sys
from parser import parser

def main(argv):
    filename = sys.argv[1]
    file = open(filename)
    data = file.read()
    file.close()

    print(data)
    parser.parse(data, tracking = True)

if __name__ == '__main__':
    main(sys.argv)