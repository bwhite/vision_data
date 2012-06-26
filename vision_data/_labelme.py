import glob
import vision_data
import re
import urllib
import zlib
import base64


class LabelMe(vision_data.VisionDataset):

    def __init__(self):
        super(LabelMe, self).__init__(name='labelme',
                                    homepage='http://labelme.csail.mit.edu',
                                    data_urls=[],
                                    bibtexs=None,
                 overview=None)

    def download(self):

        def url_dir(url):
            print(url)
            out = []
            for x in re.findall('href="([^\?/][^"]+)"', urllib.urlopen(url).read()):
                # NOTE(brandyn): We have to ignore this because it has no files and many empty dirs
                if x.find('static_web_tinyimagesdataset') != -1:
                    continue
                x = ''.join([url, x])
                if x.endswith('/'):
                    out += url_dir(x)
                else:
                    out.append(x)
            return out
        return [x for x in url_dir('http://labelme.csail.mit.edu/Annotations/') if x.endswith('.xml')]
