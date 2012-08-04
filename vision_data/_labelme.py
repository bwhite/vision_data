import glob
import vision_data
import re
import urllib
import gzip
import pickle
import os
import hashlib
import logging


def url_dir(url):
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


class LabelMe(vision_data.VisionDataset):

    def __init__(self):
        super(LabelMe, self).__init__(name='labelme',
                                    homepage='http://labelme.csail.mit.edu',
                                    data_urls=[],
                                    bibtexs=None,
                 overview=None)

    def download(self, cached=True):
        if cached:
            xml_urls = pickle.load(gzip.GzipFile('labelme_xmls.pkl.gz'))
        else:
            xml_urls = [x for x in url_dir('http://labelme.csail.mit.edu/Annotations/') if x.endswith('.xml')]
        annotation_path = self.dataset_path + '/Annotations/'
        try:
            os.makedirs(annotation_path)
        except OSError:
            pass
        for x in xml_urls:
            print(x)
            xml_data = urllib.urlopen(x).read()
            name = annotation_path + hashlib.md5(xml_data).hexdigest() + '-' + os.path.basename(x)
            open(name, 'w').write(xml_data)

    def object_rec_parse_url(self, objects=None, unique=True):
        """
        Args:
            objects: List of objects to return (if None then return all)
        
        Returns:
            Iterator of (image_url, objects), where
            objects is a list of {'class': class_name, 'xy': np_array}
        """
        objects = set(objects)
        prev_urls = set()
        for fn in glob.glob(self.dataset_path + 'Annotations/*.xml'):
            try:
                image_fn, folder, cur_objects = vision_data.parse_voc_xml(fn)
                cur_objects = [x for x in cur_objects if x['class'] in objects]
            except:
                logging.warning('Cannot parse [%s]' % fn)
            else:
                if cur_objects:
                    if (folder, image_fn) in prev_urls:
                        print('Duplicate Annotation: http://labelme.csail.mit.edu/Images/%s/%s' % (folder, image_fn))
                        continue
                    prev_urls.add((folder, image_fn))
                    print('http://labelme.csail.mit.edu/Images/%s/%s' % (folder, image_fn))
                    yield 'http://labelme.csail.mit.edu/Images/%s/%s' % (folder, image_fn), cur_objects
