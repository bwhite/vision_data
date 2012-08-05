import hadoopy
import os

def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def _chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def flickr_images(tags, images_per_tag, hdfs_output, num_files=20, api_key=None, api_secret=None, remove_output=False):
    tags = list(tags)
    if api_key is None or api_secret is None:
        api_key = os.environ['FLICKR_API_KEY']
        api_secret = os.environ['FLICKR_API_SECRET']
    tags_per_chunk = max(len(tags) / num_files, 1)
    if remove_output and hadoopy.exists(hdfs_output):
        print('Removing output dir[%s]' % hdfs_output)
        hadoopy.rmr(hdfs_output)
    for chunk_num, chunk_tags in enumerate(_chunks(tags, tags_per_chunk)):
        hadoopy.writetb(hdfs_output + '/tags/%d' % chunk_num, [(images_per_tag, tag) for tag in chunk_tags])
    hadoopy.launch_frozen(hdfs_output + '/tags', hdfs_output + '/metadata', _lf('flickr_bulk.py'), cmdenvs={'FLICKR_API_KEY': api_key,
                                                                                                            'FLICKR_API_SECRET': api_secret}, num_reducers=num_files)
    hadoopy.launch_frozen(hdfs_output + '/metadata', hdfs_output + '/image_metadata', _lf('file_downloader.py'))
