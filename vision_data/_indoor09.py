import os
import vision_data


class Indoor09(vision_data.VisionDataset):
    """
    Uses the provided dataset splits to locate the images.
    """

    def __init__(self):
        super(Indoor09, self).__init__(name='indoor09',
                                    data_urls={('5d176e5f0e56624a453f2fe0d8b19ff7',
                                                'indoorCVPR_09.tar'): ['http://groups.csail.mit.edu/vision/LabelMe/NewImages/indoorCVPR_09.tar'],
                                               ('fd987513d0f623c424252770fac3f354',
                                                'TrainImages.txt'): ['http://web.mit.edu/torralba/www/TrainImages.txt'],
                                               ('f00bef137f39d51e4894303a7bf4c2d4',
                                                'TestImages.txt'): ['http://web.mit.edu/torralba/www/TestImages.txt']},
                                    homepage='http://web.mit.edu/torralba/www/indoor.html',
                                    bibtexs=None,
                 overview=None)

    def scene_rec_parse(self, split='train'):
        """
        Args:
            split: Dataset split, one of 'train', 'test' (default: train)
        
        Returns:
            Dataset as specified by 'split'

            Data is in the form of [image_path] = scene_name
        """
        try:
            images_fn = {'train': 'TrainImages.txt', 'test': 'TestImages.txt'}[split]
        except KeyError:
            raise ValueError('Invalid split vlaue')
        out = {}
        with open(self.dataset_path + images_fn) as fp:
            for image_name in fp:
                image_name = image_name.strip()
                out['%sImages/%s' % (self.dataset_path, image_name)] = os.path.dirname(image_name)
        return out
