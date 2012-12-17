import vision_data
import hadoopy_hbase
import hashlib
import os
import json


def main(**kw):
    client = hadoopy_hbase.connect()
    table_name = 'images'
    client.createTable(table_name, [hadoopy_hbase.ColumnDescriptor('data:', maxVersions=1),
                                    hadoopy_hbase.ColumnDescriptor('meta:', maxVersions=1),
                                    hadoopy_hbase.ColumnDescriptor('pred:', maxVersions=1),
                                    hadoopy_hbase.ColumnDescriptor('srch:', maxVersions=1),
                                    hadoopy_hbase.ColumnDescriptor('attr:', maxVersions=1),
                                    hadoopy_hbase.ColumnDescriptor('misc:', maxVersions=1),
                                    hadoopy_hbase.ColumnDescriptor('feat:', maxVersions=1, compression='SNAPPY'),
                                    hadoopy_hbase.ColumnDescriptor('hash:', maxVersions=1)])
    for split_name in ['train', 'test']:
        split = (split_name, 1, -1)
        for k, hierarchy in vision_data.SUN397().scene_rec_parse(split=split).items():
            a = hadoopy_hbase.hash_key(os.path.basename(k), prefix='sun397:' + split_name, suffix=os.path.basename(k), hash_bytes=4)
            print repr(a)
            image_data = open(k).read()
            md5 = hashlib.md5(image_data).digest()
            ms = [hadoopy_hbase.Mutation(column='data:image', value=image_data),
                  hadoopy_hbase.Mutation(column='hash:md5', value=md5),
                  hadoopy_hbase.Mutation(column='meta:path', value=k)]
            for n, h in enumerate(hierarchy):
                ms.append(hadoopy_hbase.Mutation(column='meta:class_%d' % n, value=h))
            client.mutateRow(table_name, a, ms)

if __name__ == '__main__':
    main()
