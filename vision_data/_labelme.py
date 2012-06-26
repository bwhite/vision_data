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

        def url_dir(url, ignore='static_web_tinyimagesdataset'):
            print(url)
            out = []
            for x in re.findall('href="([^\?/][^"]+)"', urllib.urlopen(url).read()):
                if x.find(ignore) != -1:
                    continue
                x = ''.join([url, x])
                if x.endswith('/'):
                    out += url_dir(x)
                else:
                    out.append(x)
            return out
        return url_dir('http://labelme.csail.mit.edu/Annotations/')
