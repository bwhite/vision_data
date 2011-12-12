import glob
import vision_data
import os


class ESP(vision_data.VisionDataset):
    """
    """

    def __init__(self):
        super(ESP, self).__init__(name='esp',
                                    data_urls={('58b3a6f1b8d6ec003458f940ada226bb',
                                                'ESPGame100k.tar.gz'): ['http://server251.theory.cs.cmu.edu/ESPGame100k.tar.gz']},
                                    homepage='http://www.cs.cmu.edu/~biglou/resources/',
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
