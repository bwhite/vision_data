import vision_data
import glob


class LFWcrop(vision_data.VisionDataset):
    """
    Uses the provided dataset splits to locate the images.
    """

    def __init__(self):
        super(LFWcrop, self).__init__(name='lfwcrop',
                                      data_urls={('8a22c6c73d3d8e10a7175f5e8854e888',
                                                  'lfwcrop_color.zip'): ['http://itee.uq.edu.au/~conrad/lfwcrop/lfwcrop_color.zip']},
                                      homepage='http://itee.uq.edu.au/~conrad/lfwcrop/',
                                      bibtexs=None,
                                      overview=None)

    def images(self):
        """
        Args:
            split: Dataset split, one of 'train' or 'test' (default: train)

        Returns:
            Dataset as specified by 'split'

            Data is in the form of [(IsSame, (face0_path, face1_path)), ...]
            where IsSame is boolean.
        """
        # TODO: This is incomplete
        for split in ['train', 'test']:
            out = []
            for label in ['diff', 'same']:
                g = 'lists/*%s_%s.txt' % (split, label)
                for list_fn in glob.glob(self.dataset_path + g):
                    with open(list_fn) as list_fp:
                        for line in list_fp:
                            face0, face1 = line.strip().split()
                            face0_fn = '%sfaces/%s.ppm' % (self.dataset_path, face0)
                            face1_fn = '%sfaces/%s.ppm' % (self.dataset_path, face1)
                            out.append((label == 'same', (face0_fn, face1_fn)))
            return out
