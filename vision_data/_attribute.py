import numpy as np
import os
import glob
import cPickle as pickle
import vision_data
from PIL import Image
import re


class Attribute(vision_data.VisionDataset):
    """
    """

    def __init__(self):
        super(Attribute, self).__init__(name='attribute',
                                   data_urls={('069a586c1ab35b1fdc75ddc9d824697a',
                                               'attribute_dataset.tar.gz'): ['http://bw-school.s3.amazonaws.com/attribute_dataset.tar.gz']},
                                   homepage='http://www.image-net.org/download-attributes',
                                   bibtexs=None,
                                overview=None)

    def segmentation_boxes(self, split='all'):
        """
        Args:
            split: Dataset split, one of 'color', 'texture', 'all' (default: all)
        
        Yields:
            Dataset as specified by 'split'

            Data is in the form of (masks, PIL Image), where
            masks is a dict of boolean masks with keys as class names
        """
        assert split in ('color', 'texture', 'all')
        # n02391049_1551-white.pgm
        print(self.dataset_path + 'attrib_images')
        fns = sorted([re.search('.*/([a-zA-Z0-9_]+)\.JPEG', x).group(1)
                      for x in glob.glob(self.dataset_path + 'attrib_images/*.JPEG')])
        splits = (split,) if split != 'all' else ('color', 'texture')
        attributes_map = {}
        for split in splits:
            attributes_map[split] = sorted(set([re.search('.*/.*\-([a-zA-Z0-9]+)\.pgm', x).group(1)
                                                for x in glob.glob(self.dataset_path + split + '/*.pgm')]))
        for fn in fns:
            masks = {}
            image = Image.open('%sattrib_images/%s.JPEG' % (self.dataset_path, fn))
            width, height = image.size
            for split in splits:
                attributes = attributes_map[split]
                for attribute in attributes:
                    try:
                        masks[attribute] = np.asarray(Image.open('%s%s/%s-%s.pgm' % (self.dataset_path,
                                                                                     split, fn, attribute)))
                    except IOError:
                        masks[attribute] = np.zeros((height, width), dtype=np.uint8)
            yield masks, image

