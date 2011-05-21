import xml.etree.cElementTree as ElementTree
import numpy as np
import glob
import os
import cPickle as pickle
import vision_data


class SUN09(vision_data.VisionDataset):

    def __init__(self):
        super(SUN09, self).__init__(name='sun09',
                                    data_urls={('fd2679cddee3198976086f01eb112f1a',
                                                'sun09.tar'): ['http://groups.csail.mit.edu/vision/SUN/Hcontext/data/sun09.tar']},
                                    homepage='http://people.csail.mit.edu/myungjin/HContext.html',
                                    bibtexs=None,
                 overview=None)

    def _parse(self, xml_filename):
        # Replace a malformed character with a valid one (only one in the database)
        xml_data = open(xml_filename).read().replace('', "'")
        xml = ElementTree.fromstring(xml_data)
        filename = xml.find('filename').text.strip()
        folder = xml.find('folder').text.strip()
        objs = []
        for obj in xml.findall('object'):
            polygon = []
            for x in obj.findall('polygon'):
                polygon.append(np.array([(int(pt.find('x').text),
                                          int(pt.find('y').text))
                                         for pt in x.findall('pt')]))

            objs.append({'name': obj.find('name').text.strip(),
                         #'id': int(obj.find('id').text.strip()),
                         'polygon_xy': polygon})
        return filename, folder, objs

    def _parse_all(self):
        data = {}

        for folder_path in glob.glob(self.dataset_path + 'Annotations/*'):
            if os.path.basename(folder_path) not in ('out_of_context',
                                                     'static_sun09_database'):
                continue
            for filename_path in glob.glob(folder_path + '/*'):
                try:
                    filename, folder, objs = self._parse(filename_path)
                except Exception, e:
                    print(e)
                    print('Parse Error: %s' % filename_path)
                    continue
                assert os.path.basename(folder_path) == folder
                data.setdefault(folder, {})[filename] = objs
        static_data = {}
        for object_path in glob.glob('%s/Annotations/static_sun_objects/*' % (self.dataset_path)):
            try:
                filename, folder, objs = self._parse(filename_path)
            except Exception, e:
                print(e)
                print('Parse Error: %s' % filename_path)
                continue
            object_name = os.path.basename(object_path)
            static_data.setdefault(object_name, []).append(objs)
        return static_data, data['out_of_context'], data['static_sun09_database']

    def load(self):
        """
        Returns:
            Tuple of (static_data, out_of_context, sun09).

            Out_of_context and  are in the form of [image_path] = objects, where
            objects is {'name': class_name, 'polygon_xy': np_array}

            Static_data is in the form of [class_name][image_path] = objects,
            where objects is {'name': class_name, 'polygon_xy': np_array}

            static_data: Used for training base classifiers
            out_of_context: Out of context data
            sun09: Primary dataset, has several objects per image
        """
        pkl_fn = self.dataset_path + 'sun09.pkl'
        if not os.path.exists(pkl_fn):
            print('Performing initial parse, this takes a few minutes.')
            static_data, out_of_context, sun09 = self._parse_all()
            with open(pkl_fn, 'w') as sun09_fp:
                pickle.dump((static_data, out_of_context, sun09), sun09_fp, -1)
        else:
            with open(pkl_fn) as sun09_fp:
                static_data, out_of_context, sun09 = pickle.load(sun09_fp)
