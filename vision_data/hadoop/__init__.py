import hadoopy
import os

def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def flickr_images(tags, images_per_tag, hdfs_output):
    hadoopy.writetb(hdfs_output + '/tags', ((images_per_tag, x) for x in tags))
    hadoopy.launch_frozen(hdfs_output + '/tags', hdfs_output + '/metadata', _lf('flickr_bulk.py'))
    hadoopy.launch_frozen(hdfs_output + '/metadata', hdfs_output + '/image_metadata', _lf('file_downloader.py'))
