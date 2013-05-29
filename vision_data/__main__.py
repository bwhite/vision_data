import argparse
import vision_data


def main():
    parser = argparse.ArgumentParser(description='Vision data loader')
    subparser = parser.add_subparser('picarus', help='Load database using Picarus')
    subparser.add_argument('prefix')
    subparser.add_argument('dataset', choices=list(vision_data.DATASETS))
    subparser.add_argument('email')
    subparser.add_argument('--download', action='store_true')
    subparser.add_argument('--api_key')
    subparser.add_argument('--login_key')
    subparser.add_argument('--otp')
    subparser.add_argument('--verbose', action='store_true')
    subparser.add_argument('--test', help='Upload, get, check, delete each row (one row at a time).', action='store_true')
    subparser.add_argument('--picarus_server', default='https://api.picar.us')
    subparser.set_defaults(func=vision_data.picarus_loader)

    subparser = subparser.add_subparser('hbase', help='Load database using Picarus')
    subparser.add_argument('prefix')
    subparser.add_argument('dataset', choices=list(vision_data.DATASETS))
    subparser.add_argument('--download', action='store_true')
    subparser.add_argument('--verbose', action='store_true')
    subparser.add_argument('--thrift_server', default='localhost')
    subparser.add_argument('--thrift_port', default='9090')
    subparser.set_defaults(func=vision_data.hbase_loader)

    args = subparser.parse_args()
    kw = vars(args)
    del kw['func']
    args.func(**kw)

if __name__ == '__main__':
    main()
