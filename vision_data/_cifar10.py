import glob
import vision_data
import os
import cPickle as pickle
import cv2
import numpy as np


class CIFAR10(vision_data.VisionDataset):
    """
    """

    def __init__(self):
        super(CIFAR10, self).__init__(name='cifar10',
                                    data_urls={('c58f30108f718f92721af3b95e74349a',
                                                'cifar-10-python.tar.gz'): ['http://www.cs.utoronto.ca/~kriz/cifar-10-python.tar.gz']},
                                    homepage='http://www.cs.utoronto.ca/~kriz/cifar.html',
                                    bibtexs=None,
                 overview=None)

    def single_image_class_boxes(self, split='train'):
        """
        Returns:
        
        """
        if split == 'train':
            paths = [self.dataset_path + '/cifar-10-batches-py/data_batch_%d' % x
                     for x in range(1, 6)]
        elif split == 'test':
            paths = [self.dataset_path + '/cifar-10-batches-py/test_batch']
        else:
            raise ValueError('split must be train or test!')
        label_names = pickle.load(open(self.dataset_path + '/cifar-10-batches-py/batches.meta'))['label_names']
        for path in paths:
            with open(path) as fp:
                batch_data = pickle.load(fp)
                image_data = batch_data['data']
                image_data = image_data.reshape((image_data.shape[0], 3, 32, 32))
                image_data = image_data[:, ::-1, :, :]  # RGB to BGR
                image_data = np.ascontiguousarray(image_data.swapaxes(1, 2).swapaxes(2, 3))
                for object_class, image in zip(batch_data['labels'], image_data):
                    yield label_names[object_class], image

