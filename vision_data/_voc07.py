import vision_data
import glob
import re
import os


class VOC07(vision_data.VisionDataset):
    """
    """
    def __init__(self):
        super(VOC07, self).__init__(name='voc07',
                                    data_urls={('b6e924de25625d8de591ea690078ad9f',
                                                'VOCtest_06-Nov-2007.tar'): ['http://pascallin.ecs.soton.ac.uk/challenges/VOC/voc2007/VOCtest_06-Nov-2007.tar'],
                                               ('c52e279531787c972589f7e41ab4ae64',
                                                'VOCtrainval_06-Nov-2007.tar'): ['http://pascallin.ecs.soton.ac.uk/challenges/VOC/voc2007/VOCtrainval_06-Nov-2007.tar']},
                                    homepage='http://pascallin.ecs.soton.ac.uk/challenges/VOC/voc2007/index.html',
                                    bibtexs=None,
                 overview=None)

    def image_class_negpos_parse(self, split='train'):
        """
        Args:
            split: Dataset split, one of 'train', 'trainval', 'val', 'test' (default: train)
        
        Returns:
            Dataset as specified by 'split'
            Data is in the form of [image_path] = (neg_image_classes, pos_image_classes) where each is a set of strings
        """
        assert split in ('train', 'trainval', 'val', 'test')
        data = {}
        image_name_to_path = lambda x: '%s/VOCdevkit/VOC2007/JPEGImages/%s.jpg' % (self.dataset_path, x)
        for fn in glob.glob(self.dataset_path + '/VOCdevkit/VOC2007/ImageSets/Main/*_%s.txt' % split):
            class_name = re.search('([a-z]+)_(train|trainval|val|test)\.txt', os.path.basename(fn)).group(1)
            for x in open(fn):
                image_name, polarity = x.rstrip().split()
                polarity = 1 if polarity == '1' else 0
                data.setdefault(image_name_to_path(image_name), ([], []))[polarity].append(class_name)
        return data
            
        
