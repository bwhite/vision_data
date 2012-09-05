import glob
import vision_data
import json


class SUN397(vision_data.VisionDataset):
    """
    Uses the provided dataset splits to locate the images.
    """
    def __init__(self):
        super(SUN397, self).__init__(name='sun397',
                                    data_urls={('58b3a6f1b8d6ec003458f940ada226bb',
                                                'SUN397.tar'): ['http://groups.csail.mit.edu/vision/SUN1old/SUN397.tar',
                                                                'http://bozo.csail.mit.edu/SUN/SUN397.tar'],
                                               ('29a205c0a0129d21f36cbecfefe81881',
                                                'Partitions.zip'): ['http://people.csail.mit.edu/jxiao/SUN/download/Partitions.zip'],
                                               ('7d9184832f741857126697e11b5485bf', 'sun908_hierarchy.js'): ['http://bw-school.s3.amazonaws.com/sun908_hierarchy.js']
                                               },
                                    homepage='http://groups.csail.mit.edu/vision/SUN/',
                                    bibtexs=None,
                 overview=None)
        self.hierarchy = None

    def scene_rec_parse(self, split=('train', 1, 2)):
        """
        Args:
            split: Dataset split, one of 'train', 'test' (default: train) or
                (split, partition, level) where partition is an integer [1,10]
                and level of the hierarchy to report [0, 2]
        Returns:
            Dataset as specified by 'split'

            Data is in the form of [image_path] = scene_name
        """
        if self.hierarchy is None:
            self.hierarchy = json.load(open(self.dataset_path + 'sun908_hierarchy.js'))
        split, partition, level = split
        assert 0 < partition <= 10
        assert 0 <= level <= 2
        partition = '%.2d' % partition
        if split == 'train':
            g = 'Training_%s.txt' % partition
        elif split == 'test':
            g = 'Testing_%s.txt' % partition
        else:
            raise ValueError('Invalid split vlaue')
        out = {}
        print(self.dataset_path + g)
        for images_fn in glob.glob(self.dataset_path + g):
            print(images_fn)
            with open(images_fn) as fp:
                for image_name in fp:
                    image_name = image_name.strip()
                    class_name = image_name.split('/', 2)[-1].rsplit('/', 1)[0]
                    if level < 2:
                        class_name = self.hierarchy[class_name][level]
                    out['%sSUN397%s' % (self.dataset_path, image_name)] = class_name
        return out
