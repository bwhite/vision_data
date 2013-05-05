import vision_data
import hadoopy_hbase
import argparse


DATASETS = {'CIFAR10': vision_data.CIFAR10, 'SUN397': vision_data.SUN397, 'LFWFunneling': vision_data.LFWFunneling}
TABLE = 'images'


def main(prefix, dataset, thrift_server, thrift_port):
    dataset = DATASETS[dataset]()
    client = hadoopy_hbase.connect(thrift_server, thrift_port)
    for split, name, columns in dataset.images():
        row = hadoopy_hbase.hash_key(name, prefix=prefix + split, suffix=name, hash_bytes=4)
        print(repr(row))
        mutations = [hadoopy_hbase.Mutation(column=x, value=y) for x, y in columns.items()]
        client.mutateRow(TABLE, row, mutations)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Vision data loader')
    parser.add_argument('prefix')
    parser.add_argument('dataset', choices=list(DATASETS))
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--thrift_server', default='localhost')
    parser.add_argument('--thrift_port', default='9090')
    ARGS = parser.parse_args()
    main(ARGS.prefix, ARGS.dataset, ARGS.thrift_server, ARGS.thrift_port)
