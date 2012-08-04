import hadoopy
import os

def _lf(fn):
    from . import __path__
    return os.path.join(__path__[0], fn)


def flickr_images(tags, images_per_tag, hdfs_output, api_key=None, api_secret=None):
    if api_key is None or api_secret is None:
        api_key = os.environ['FLICKR_API_KEY']
        api_secret = os.environ['FLICKR_API_SECRET']
    hadoopy.writetb(hdfs_output + '/tags', ((images_per_tag, x) for x in tags))
    hadoopy.launch_frozen(hdfs_output + '/tags', hdfs_output + '/metadata', _lf('flickr_bulk.py'), cmdenvs={'FLICKR_API_KEY': api_key,
                                                                                                            'FLICKR_API_SECRET': api_secret})
    hadoopy.launch_frozen(hdfs_output + '/metadata', hdfs_output + '/image_metadata', _lf('file_downloader.py'))
