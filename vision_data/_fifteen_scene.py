import glob
import vision_data
import re


class FifteenScene(vision_data.VisionDataset):
    """
    """

    def __init__(self):
        super(FifteenScene, self).__init__(name='fifteen_scene',
                                    data_urls={('58828019197b2ad0a7efb472e7a85c2a',
                                                'scene_categories.zip'): ['http://www-cvr.ai.uiuc.edu/ponce_grp/data/scene_categories/scene_categories.zip']},
                                    homepage='http://www-cvr.ai.uiuc.edu/ponce_grp/data/',
                                    bibtexs=None,
                 overview=None)

    def scene_rec_parse(self):
        """
        Returns:
            Dataset as specified by 'split'

            Data is in the form of [image_path] = scene_name
        """
        out = {}
        for full_class_path in glob.glob(self.dataset_path + '/*'):
            class_name = re.search('.*/[A-Z]*([a-z]+)$', full_class_path).group(1)
            for x in glob.glob(full_class_path + '/*.jpg'):
                out[x] = class_name
        return out

