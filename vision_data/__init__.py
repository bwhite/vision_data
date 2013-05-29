from _base import VisionDataset, parse_voc_xml
from _sun09 import SUN09
from _sun397 import SUN397
from _indoor09 import Indoor09
from _lfwcropped import LFWcrop
from _lfwfunneling import LFWFunneling
from _caltech256 import Caltech256
from _msrc import MSRC
from _voc07 import VOC07
from _esp import ESP
from _fifteen_scene import FifteenScene
from _attribute import Attribute
from _cifar10 import CIFAR10
from _cifar100 import CIFAR100
from _imagenet import ImageNet
from _labelme import LabelMe
from _flickr import Flickr


DATASETS = {'CIFAR10': CIFAR10, 'SUN397': SUN397,
            'LFWFunneling': LFWFunneling, 'Caltech256': Caltech256}
TABLE = 'images'


def hbase_loader(prefix, dataset, thrift_server, thrift_port, verbose=False):
    import hadoopy_hbase
    dataset = DATASETS[dataset]()
    client = hadoopy_hbase.connect(thrift_server, thrift_port)
    for split, name, columns in dataset.images():
        row = hadoopy_hbase.hash_key(name, prefix=prefix + split, suffix=name, hash_bytes=4)
        if verbose:
            print(repr(row))
        mutations = [hadoopy_hbase.Mutation(column=x, value=y) for x, y in columns.items()]
        client.mutateRow(TABLE, row, mutations)


def picarus_loader(prefix, dataset, email, picarus_server, api_key=None, login_key=None, otp=None, download=False, test=False, verbose=False):
    import hadoopy_hbase
    import picarus
    dataset = DATASETS[dataset]()
    if download:
        dataset.download()
    if otp:
        api_key = picarus.PicarusClient(email=email, login_key=login_key, server=picarus_server).auth_yubikey(otp)['apiKey']
    if api_key is None:
        raise ValueError('api_key or login_key/otp must be set!')
    client = picarus.PicarusClient(email=email, api_key=api_key, server=picarus_server, max_attempts=10)
    for split, name, columns in dataset.images():
        row = hadoopy_hbase.hash_key(name, prefix=prefix + split, suffix=name, hash_bytes=4)
        if verbose:
            print('row[%r] len(data:image)[%d]' % (repr(row), len(columns.get('data:image', ''))))
        client.patch_row(TABLE, row, columns)
        if test:
            remote_columns = client.get_row(TABLE, row)
            if remote_columns != columns:
                print(remote_columns)
                print(columns)
                print({x: len(y) for x, y in remote_columns.items()})
                print({x: len(y) for x, y in columns.items()})
                assert remote_columns == columns
            client.delete_row(TABLE, row)
