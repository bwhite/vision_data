import vision_data
import os
import cPickle as pickle
import numpy as np


class CIFAR10(vision_data.VisionDataset):

    def __init__(self):
        super(CIFAR10, self).__init__(name='cifar10',
                                      data_urls={('c58f30108f718f92721af3b95e74349a',
                                                  'cifar-10-python.tar.gz'): ['http://www.cs.utoronto.ca/~kriz/cifar-10-python.tar.gz']},
                                      homepage='http://www.cs.utoronto.ca/~kriz/cifar.html',
                                      bibtexs=None,
                                      overview=None)

    def images(self):
        import cv2
        prefix_paths = [('train', self.dataset_path + '/cifar-10-batches-py/data_batch_%d' % x)
                        for x in range(1, 6)]
        prefix_paths += [('test', self.dataset_path + '/cifar-10-batches-py/test_batch')]
        label_names = pickle.load(open(self.dataset_path + '/cifar-10-batches-py/batches.meta'))['label_names']
        for prefix, path in prefix_paths:
            with open(path) as fp:
                batch_data = pickle.load(fp)
                image_datas = batch_data['data']
                image_datas = image_datas.reshape((image_datas.shape[0], 3, 32, 32))
                image_datas = image_datas[:, ::-1, :, :]  # RGB to BGR
                image_datas = np.ascontiguousarray(image_datas.swapaxes(1, 2).swapaxes(2, 3))
                fn = os.path.basename(path)
                for num, (label, image_data) in enumerate(zip(batch_data['labels'], image_datas)):
                    image_data = cv2.imencode('.ppm', image_data)[1].tostring()
                    yield prefix, '%s_%.5d' % (fn, num), {'data:image': image_data, 'meta:class': label_names[label]}
