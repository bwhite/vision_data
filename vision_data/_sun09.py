import xml.etree.cElementTree as ElementTree
import numpy as np
import glob
import os
import cPickle as pickle
import vision_data
import scipy as sp
import scipy.io


class SUN09(vision_data.VisionDataset):
    """

    Loads the ground truth from the .mat as it has been post-processed, the
    .xml files are fairly dirty.  The code to parse them is included but not
    used by default.
    """

    def __init__(self):
        super(SUN09, self).__init__(name='sun09',
                                    data_urls={('fd2679cddee3198976086f01eb112f1a',
                                                'sun09.tar'): ['http://groups.csail.mit.edu/vision/SUN/Hcontext/data/sun09.tar'],
                                               ('d8f02fef3872cfad10e76c10927f47ef',
                                                'datasetMat.tar'): ['http://groups.csail.mit.edu/vision/SUN/Hcontext/data/datasetMat.tar']},
                                    homepage='http://people.csail.mit.edu/myungjin/HContext.html',
                                    bibtexs=None,
                 overview=None)

    def _parse_xml(self, xml_filename):
        # Replace a malformed character with a valid one (only one in the database)
        xml_data = open(xml_filename).read().replace('', "'")
        xml = ElementTree.fromstring(xml_data)
        filename = xml.find('filename').text.strip()
        folder = xml.find('folder').text.strip()
        objs = []
        for obj in xml.findall('object'):
            polygon = []
            x = obj.find('polygon')
            polygon = np.array([(int(pt.find('x').text),
                                 int(pt.find('y').text))
                                for pt in x.findall('pt')])
            objs.append({'class': obj.find('name').text.strip(),
                         #'id': int(obj.find('id').text.strip()),
                         'xy': polygon})
        return filename, folder, objs

    def _parse_xml_all(self):
        data = {}

        for folder_path in glob.glob(self.dataset_path + 'Annotations/*'):
            if os.path.basename(folder_path) not in ('out_of_context',
                                                     'static_sun09_database'):
                continue
            image_path = self.dataset_path + 'Images/%s/' % os.path.basename(folder_path)
            for filename_path in glob.glob(folder_path + '/*'):
                try:
                    filename, folder, objs = self._parse_xml(filename_path)
                except Exception, e:
                    print(e)
                    print('Parse Error: %s' % filename_path)
                    continue
                assert os.path.basename(folder_path) == folder
                data.setdefault(folder, {})[image_path + filename] = objs
        static_data = {}
        for object_path in glob.glob('%s/Annotations/static_sun_objects/*' % (self.dataset_path)):
            image_path = self.dataset_path + 'Images/static_sun_objects/'
            try:
                filename, folder, objs = self._parse_xml(filename_path)
            except Exception, e:
                print(e)
                print('Parse Error: %s' % filename_path)
                continue
            object_name = os.path.basename(object_path)
            static_data.setdefault(object_name, []).append(objs)
        return static_data, data['out_of_context'], data['static_sun09_database']

    def _parse_mat_dataset(self, dataset):
        image_objects = {}
        for cur_image_data in dataset:
            cur_image_data = cur_image_data.annotation[0][0]
            filename = ''.join(cur_image_data.filename[0])
            directory = ''.join(cur_image_data.folder[0])
            img_path = '%s%s/%s' % (self.dataset_path, directory, filename)
            image_objects[img_path] = []
            for obj in cur_image_data.object[0]:
                class_name = ''.join(obj.name[0])
                x = obj.polygon[0][0].x
                y = obj.polygon[0][0].y
                xy = np.hstack([x, y])
                image_objects[img_path].append({'class_name': class_name,
                                                'xy': xy})
        return image_objects

    def _parse_mat(self):
        data = sp.io.loadmat('%sdataset/sun09_groundTruth.mat' % self.dataset_path,
                             chars_as_strings=False, struct_as_record=False)
        train_image_objects = self._parse_mat_dataset(data['Dtraining'][0])
        test_image_objects = self._parse_mat_dataset(data['Dtest'][0])
        return train_image_objects, test_image_objects

    def object_rec_parse(self, split='train'):
        """
        Args:
            split: Dataset split, one of 'train', 'test' (default: train)
        
        Returns:
            Dataset as specified by 'split'

            Data is in the form of [image_path] = objects, where
            objects is {'class': class_name, 'xy': np_array}
        """
        pkl_fn = self.dataset_path + 'sun09.pkl'
        if not os.path.exists(pkl_fn):
            print('Performing initial parse, this takes a minute.')
            train_data, test_data = self._parse_mat()
            with open(pkl_fn, 'w') as sun09_fp:
                pickle.dump((train_data, test_data), sun09_fp, -1)
        else:
            with open(pkl_fn) as sun09_fp:
                train_data, test_data = pickle.load(sun09_fp)
        if split == 'train':
            return train_data
        elif split == 'test':
            return test_data
        else:
            raise ValueError('Invalid split vlaue')
