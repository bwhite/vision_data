import vision_data
import glob
import re
import os


class Caltech256(vision_data.VisionDataset):
    """
    Uses the provided dataset splits to locate the images.
    """

    def __init__(self):
        super(Caltech256, self).__init__(name='caltech256',
                                         data_urls={('67b4f42ca05d46448c6bb8ecd2220f6d',
                                                     '256_ObjectCategories.tar'): ['http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar']},
                                         homepage='http://www.vision.caltech.edu/Image_Datasets/Caltech256/',
                                         bibtexs=None,
                                         overview=None)

    def images(self):
        for class_name_enc in glob.glob(self.dataset_path + '/256_ObjectCategories/*'):
            class_name = re.search(r'.+256_ObjectCategories/[0-9]+\.([a-z\-]+[a-z])(\-101)?', class_name_enc).group(1)
            for fn in glob.glob(class_name_enc + '/*.jpg'):
                yield '', os.path.basename(fn), {'meta:class': class_name, 'data:image': open(fn).read()}
