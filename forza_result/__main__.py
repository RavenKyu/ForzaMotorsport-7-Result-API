import argparse
from forza_result import convert
from forza_result.app import app

def argument_parser():
    parser = argparse.ArgumentParser('table-ocr')
    parser.add_argument('-f', '--image_path', type=str)
    parser.add_argument('-a', '--address', default='localhost',
                        help='host address')
    parser.add_argument('-p', '--port', type=int, default=5000,
                        help='port')
    parser.add_argument('-d', '--debug', action='store_true')
    return parser


def main():
    parser = argument_parser()
    argspec = parser.parse_args()

    if argspec.image_path:
        value = convert(image_file=argspec.image_path, data='')
        print(value)
        return

    app.run(host=argspec.address,
            port=argspec.port,
            debug=argspec.debug)


if __name__ == '__main__':
    main()

