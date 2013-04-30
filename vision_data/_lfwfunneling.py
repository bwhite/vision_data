import vision_data
import glob
import os


class LFWFunneling(vision_data.VisionDataset):

    def __init__(self):
        super(LFWFunneling, self).__init__(name='lfwfunneling',
                                           data_urls={('1b42dfed7d15c9b2dd63d5e5840c86ad',
                                                       'lfw-funneled.tgz'): ['http://vis-www.cs.umass.edu/lfw/lfw-funneled.tgz']},
                                           homepage='http://vis-www.cs.umass.edu/lfw/',
                                           bibtexs=None,
                                           overview=None)

    def images(self):
        for p in glob.glob(self.dataset_path + '/lfw_funneled/*'):
            for y in glob.glob(p + '/*'):
                yield '', os.path.basename(p), {'meta:file': os.path.basename(y), 'meta:class': os.path.basename(p), 'data:image': open(y).read()}
