import glob
import vision_data
import json
import os


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

    def images(self, partition=1):
        """
        Args:
            partition: integer [1,10]
        """
        if self.hierarchy is None:
            self.hierarchy = json.load(open(self.dataset_path + 'sun908_hierarchy.js'))
        assert 0 < partition <= 10
        partition = '%.2d' % partition
        for split, g in [('train', 'Training_%s.txt' % partition), ('test', 'Testing_%s.txt' % partition)]:
            for images_fn in glob.glob(self.dataset_path + g):
                with open(images_fn) as fp:
                    for image_name in fp:
                        image_name = image_name.strip()
                        class_name = image_name.split('/', 2)[-1].rsplit('/', 1)[0]
                        class_name = self.hierarchy[class_name] + [class_name]
                        k = '%sSUN397%s' % (self.dataset_path, image_name)
                        columns = {'data:image': open(k).read()}
                        for x, y in enumerate(class_name):
                            columns['meta:class_%d' % x] = y
                        yield split, os.path.basename(k), columns
