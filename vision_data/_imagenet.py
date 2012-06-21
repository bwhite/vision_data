import os
import vision_data
import glob


class ImageNet(vision_data.VisionDataset):
    """
    Uses the provided dataset splits to locate the images.
    """

    def __init__(self):
        burl = 'http://www.image-net.org/archive'
        super(ImageNet, self).__init__(name='imagenet',
                                       data_urls={('',
                                                   'imagenet_fall11_urls.tgz'): [burl + '/imagenet_fall11_urls.tgz'],
                                                  ('',
                                                   'imagenet_winter11_urls.tgz'): [burl + '/imagenet_winter11_urls.tgz'],
                                                  ('',
                                                   'imagenet_spring10_urls.tgz'): [burl + '/imagenet_spring10_urls.tgz'],
                                                  ('',
                                                   'imagenet_fall09_urls.tgz'): [burl + '/imagenet_fall09_urls.tgz'],
                                                  ('',
                                                   'Annotation.tar.gz'): ['http://www.image-net.org/Annotation/Annotation.tar.gz'],
                                                  ('',
                                                   'words.txt'): [burl + '/words.txt'],
                                                  ('',
                                                   'gloss.txt'): [burl + '/gloss.txt']
                                                  },
                                    homepage='http://www.image-net.org',
                                    bibtexs=None,
                 overview=None)

    def download(self):
        if super(ImageNet, self).download():
            return True
        for fn in glob.glob(self.dataset_path + '/n*.tar.gz'):
            self._unpack_remove_file(os.path.basename(fn))

    def object_rec_parse(self, wnid='n00007846'):
        """
        Args:
            split: Dataset split, one of 'train', 'test' (default: train)
        
        Returns:
            Dataset as specified by 'split'

            Data is in the form of [image_path] = objects, where
            objects is a list of {'class': class_name, 'xy': np_array}
        """
        print glob.glob(self.dataset_path + 'Annotation/%s/*.xml' % wnid)
        return 
        if not os.path.exists(pkl_fn):
            print('Performing initial parse, this takes a minute.')
            train_data, test_data = self._parse_mat()
            with open(pkl_fn, 'w') as sun09_fp:
                pickle.dump((train_data, test_data), sun09_fp, -1)
        else:
            with open(pkl_fn) as sun09_fp:
                train_data, test_data = pickle.load(sun09_fp)
        mk_abs = lambda z: dict((self.dataset_path + x, y) for x, y in z.items())
        if split == 'train':
            return mk_abs(train_data)
        elif split == 'test':
            return mk_abs(test_data)
        else:
            raise ValueError('Invalid split vlaue')
