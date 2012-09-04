import numpy as np
import os
import cPickle as pickle
import vision_data
import Image
import cv2


class MSRC(vision_data.VisionDataset):
    """
    """

    def __init__(self):
        super(MSRC, self).__init__(name='msrc',
                                   data_urls={('8fcd292c7f1e69f91a2ef513746bd52c',
                                               'msrc_objcategimagedatabase_v2.zip'): ['http://research.microsoft.com/en-us/um/people/antcrim/data_objrec/msrc_objcategimagedatabase_v2.zip'],
                                              ('4d392500f08030b410f6d8c521b9f4c3', 'TextonBoostSplits.zip'): ['http://jamie.shotton.org/work/data/TextonBoostSplits.zip']},
                                   homepage='http://research.microsoft.com/en-us/projects/objectclassrecognition/',
                                   bibtexs=None,
                                overview=None)


    def _gt_to_masks(self, gt):
        pixel_names = {(0, 0, 128): 'cow',
                       (0, 64, 0): 'bird',
                       (0, 128, 0): 'grass',
                       (0, 128, 128): 'sheep',
                       (0, 192, 0): 'chair',
                       (0, 192, 128): 'cat',
                       (64, 0, 128): 'car',
                       (64, 64, 0): 'body',
                       (64, 128, 0): 'water',
                       (64, 128, 128): 'flower',
                       (128, 0, 0): 'building',
                       (128, 64, 0): 'book',
                       (128, 64, 128): 'road',
                       (128, 128, 0): 'tree',
                       (128, 128, 128): 'sky',
                       (128, 192, 128): 'dog',
                       (192, 0, 0): 'aeroplane',
                       (192, 0, 128): 'bicycle',
                       (192, 64, 0): 'boat',
                       (192, 128, 0): 'face',
                       (192, 128, 128): 'sign'}
        masks = {}
        for i in range(gt.shape[0]):
            for j in range(gt.shape[1]):
                try:
                    cur_class_name = pixel_names[tuple(gt[i, j, :])]
                    if cur_class_name not in masks:
                        masks[cur_class_name] = np.zeros((gt.shape[0], gt.shape[1]), dtype=np.uint8)
                    masks[cur_class_name][i, j] = 255
                except KeyError:
                    pass
        return masks

    def segmentation_boxes(self, split='train'):
        """
        Args:
            split: Dataset split, one of 'train', 'test' (default: train)
        
        Yields:
            Dataset as specified by 'split'

            Data is in the form of (masks, PIL Image), where
            masks is a dict of boolean masks with keys as class names
        """
        data_fn = {'train': 'Train.txt', 'test': 'Test.txt', 'validation': 'Validation.txt'}[split]
        with open(self.dataset_path + data_fn) as fp:
            for fn in fp:
                fn = fn.rstrip()[:-4]
                gt = np.asarray(Image.open(self.dataset_path + 'MSRC_ObjCategImageDatabase_v2/GroundTruth/%s_GT.bmp' % fn)).copy()
                image = cv2.imread(self.dataset_path + 'MSRC_ObjCategImageDatabase_v2/Images/%s.bmp' % fn)
                yield self._gt_to_masks(gt), image
