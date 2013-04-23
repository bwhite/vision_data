import vision_data
import hadoopy_hbase


DATASETS = {'CIFAR10': vision_data.CIFAR10}
TABLE = 'images'


def main(prefix, dataset):
    dataset = DATASETS[dataset]()
    client = hadoopy_hbase.connect()
    for split, name, columns in dataset.images():
        row = hadoopy_hbase.hash_key(name, prefix=prefix + split, suffix=name, hash_bytes=4)
        print(repr(row))
        mutations = [hadoopy_hbase.Mutation(column=x, value=y) for x, y in columns.items()]
        client.mutateRow(TABLE, row, mutations)

if __name__ == '__main__':
    main('cifar10:', 'CIFAR10')
