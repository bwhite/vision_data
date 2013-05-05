import hadoopy_hbase
import argparse
from load_hbase import DATASETS, TABLE
import picarus


def main(prefix, dataset, email, picarus_server, api_key=None, login_key=None, otp=None, download=False):
    dataset = DATASETS[dataset]()
    if download:
        dataset.download()
    if otp:
        api_key = picarus.PicarusClient(email=email, login_key=login_key, server=picarus_server).auth_yubikey(otp)['apiKey']
    if api_key is None:
        raise ValueError('api_key or login_key/otp must be set!')
    client = picarus.PicarusClient(email=email, api_key=api_key, server=picarus_server)
    for split, name, columns in dataset.images():
        row = hadoopy_hbase.hash_key(name, prefix=prefix + split, suffix=name, hash_bytes=4)
        print(repr(row))
        client.patch_row(TABLE, row, columns)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Vision data loader')
    parser.add_argument('prefix')
    parser.add_argument('dataset', choices=list(DATASETS))
    parser.add_argument('email')
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--api_key')
    parser.add_argument('--login_key')
    parser.add_argument('--otp')
    parser.add_argument('--picarus_server', default='https://api.picar.us')
    main(**vars(parser.parse_args()))
