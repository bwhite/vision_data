import glob
import vision_data
import os


class CIFAR100(vision_data.VisionDataset):
    """
    """

    def __init__(self):
        super(CIFAR100, self).__init__(name='cifar100',
                                    data_urls={('eb9058c3a382ffc7106e4002c42a8d85',
                                                'cifar-100-python.tar.gz'): ['http://www.cs.utoronto.ca/~kriz/cifar-100-python.tar.gz']},
                                    homepage='http://www.cs.utoronto.ca/~kriz/cifar.html',
                                    bibtexs=None,
                 overview=None)

    def image_class_parse(self):
        """
        Returns:
            Data is in the form of [image_path] = image_classes
        """
        out = {}
        for image_path in glob.glob(self.dataset_path + '/ESPGame100k/originals/*.jpg'):
            image_name = os.path.basename(image_path)
            out[image_path] = [x.rstrip() for x in open(self.dataset_path + '/ESPGame100k/labels/%s.desc' % image_name)]
        return out
