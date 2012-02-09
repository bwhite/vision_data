import hashlib
import os
import urllib
import subprocess
import shutil
import Image
import numpy as np


class DontRemoveException(Exception):
    """Raise this in the unpack_download if you don't want a file to be removed"""


class VisionDataset(object):
    """
    """
    
    def __init__(self, name, data_urls, homepage=None, bibtexs=None,
                 overview=None):
        """
        
        Args:
            name: Dataset name (e.g., voc07, sun09)
            data_urls: Dictionary with keys as (md5_hash, file_name),
                values as lists of urls.  The urls are redundant and are
                attempted in order.
            homepage: A webpage describing the dataset.
            bibtexs: A list of recommended bibtex entries
            overview: A string describing the dataset
        """
        try:
            self._data_root = os.path.abspath(os.environ['VISION_DATA_ROOT'])
        except KeyError:
            raise KeyError('Environmental variable VISION_DATA_ROOT must be set '
                           'to the path where you want to store the data files.')
        self._name = name
        self._data_urls = data_urls
        self._homepage = homepage
        self._bibtexs = bibtexs
        self._overview = overview
        self.dataset_path = '%s/%s/' % (self._data_root, self._name)

    def _unpack_download(self, file_name):
        ext = file_name.split('.', 1)[1]
        dir_name = os.path.dirname(file_name)
        if ext == 'tar':
            cmd = 'tar -xf %s -C %s' % (file_name, dir_name)
        elif ext == 'tar.gz':
            cmd = 'tar -xzf %s -C %s' % (file_name, dir_name)
        elif ext == 'tar.bz2':
            cmd = 'tar -xjf %s -C %s' % (file_name, dir_name)
        elif ext == 'zip':
            cmd = 'unzip %s -d %s' % (file_name, dir_name)
        elif ext == 'txt':  # Don't do anything
            raise DontRemoveException
        else:
            raise ValueError('Extension [%s] not supported' % ext)
        subprocess.call(cmd.split())

    def download(self, force=False):
        if force:
            print('Removing [%s]' % self.dataset_path)
            try:
                shutil.rmtree(self.dataset_path)
            except OSError, e:
                print(e)
        if os.path.exists(self.dataset_path):
            return True
        os.makedirs(self.dataset_path)
        for (md5hash, file_name), urls in self._data_urls.items():
            print('Downloading [%s]' % file_name)
            for url in urls:
                # TODO: Make this more robust and check hash
                a = urllib.urlretrieve(url, self.dataset_path + file_name)
                print(a)
                #assert(md5hash == hashlib.md5(data).hexdigest())
                break
        for (md5hash, file_name), urls in self._data_urls.items():
            print('Unpacking [%s]' % file_name)
            try:
                self._unpack_download(self.dataset_path + file_name)
            except DontRemoveException:
                pass
            else:
                print('Removing Temporary File [%s]' % file_name)
                os.remove(self.dataset_path + file_name)

    def object_rec_parse(self, *args, **kw):
        raise NotImplementedError

    def scene_rec_parse(self, *args, **kw):
        raise NotImplementedError

    def image_class_parse(self, *args, **kw):
        """
        Args:
            split: Dataset split, one of 'train', 'test' (default: train)
        
        Returns:
            Dataset as specified by 'split'
            Data is in the form of [image_path] = image_classes
        """
        try:
            return dict((x, [y]) for x, y in
                        self.scene_rec_parse(*args, **kw).items())
        except NotImplementedError:
            raise

    def image_class_negpos_parse(self, *args, **kw):
        """By default collect all tags and the negative for an image is everything not positive.

        NOTE(brandyn): If the splits are missing some of the classes then the negatives will
        be incomplete.

        Returns:
            Data is in the form of [image_path] = (neg_image_classes, pos_image_classes) where each is a set of strings
        """
        data = self.image_class_parse(*args, **kw)
        negs = set()
        for x in data.values():
            negs.update(set(x))
        return dict((x, (negs - set(y), set(y))) for x, y in data.items())

    def face_verification_parse(self, *args, **kw):
        raise NotImplementedError

    def object_rec_boxes(self, *args, **kw):
        """
        Yields:
            (object_class, PIL Image)
        """
        for image_path, objects in self.object_rec_parse(*args, **kw).items():
            image = Image.open(image_path)
            print(image_path)
            for obj in objects:
                obj['xy'] = np.ascontiguousarray(obj['xy'])
                min_coords = np.max([[0, 0],
                                     np.min(obj['xy'], 0)], 0)
                if (min_coords > image.size).any():
                    print('Warning: Annotation entirely outside of image, skipping! file[%s] class[%s] xy[%s]' % (image_path,
                                                                                                                  obj['class'],
                                                                                                                  obj['xy']))
                    continue
                max_coords = np.min([np.array(image.size) - 1,
                                     np.max(obj['xy'], 0) + 1], 0)
                left, upper = np.asarray(np.round(min_coords), dtype=np.int32)
                right, lower = np.asarray(np.round(max_coords), dtype=np.int32)
                print((left, upper, right, lower))
                print(image.size)
                yield obj['class'], image.crop((left, upper, right, lower))

    def scene_rec_boxes(self, *args, **kw):
        """
        Yields:
            (scene_name, PIL Image)
        """
        for image_path, scene_name in self.scene_rec_parse(*args, **kw).items():
            yield scene_name, Image.open(image_path)

    def face_verification_boxes(self, *args, **kw):
        """
        Yields:
            (IsSame, (face0, face1)) where face0/1 are PIL Images
        """
        for is_same, (face0_fn, face1_fn) in self.face_verification_parse(*args, **kw).items():
            yield is_same, (Image.open(face0_fn), Image.open(face1_fn))

    def image_class_boxes(self, *args, **kw):
        """
        Yields:
            (tags, PIL Image)
        """
        # If image classification data is available then use it
        try:
            image_class_data = self.image_class_parse(*args, **kw)
        except NotImplementedError:
            pass
        else:
            for image_path, tags in image_class_data.items():
                yield set(tags), Image.open(image_path)
            return
        # Else if object recognition data is available then use it
        try:
            object_rec_data = self.object_rec_parse(*args, **kw)
        except NotImplementedError:
            pass
        else:
            for image_path, objects in object_rec_data.items():
                yield set([x['class'] for x in objects]), Image.open(image_path)
            return
        # Else if scene recognition data is available then use it
        try:
            scene_rec_data = self.scene_rec_parse(*args, **kw)
        except NotImplementedError:
            pass
        else:
            for image_path, scene_name in scene_rec_data.items():
                yield set([scene_name]), Image.open(image_path)
            return
        raise NotImplementedError

    def image_class_negpos_boxes(self, *args, **kw):
        """
        Yields:
            (tags, PIL Image)
        """
        image_class_data = self.image_class_negpos_parse(*args, **kw)
        for image_path, (neg_tags, pos_tags) in image_class_data.items():
                yield (set(neg_tags), set(pos_tags)), Image.open(image_path)

    def segmentation_boxes(self, *args, **kw):
        """
        Args:
            split: Dataset split, one of 'train', 'test' (default: train)
        
        Yields:
            Dataset as specified by 'split'

            Data is in the form of (masks, PIL Image), where
            masks is a dict of boolean masks with keys as class names
        """
        import cv2
        for image_path, image_datas in self.object_rec_parse(*args, **kw).items():
            image = Image.open(image_path)
            image_arr = np.asarray(image)
            masks = {}
            for image_data in image_datas:
                c = image_data['class']
                if c not in masks:
                    masks[c] = np.zeros(image_arr.shape[:2], dtype=np.uint8)
                xy = image_data['xy']
                xy = np.array([np.vstack([xy, xy[0, :]])], dtype=np.int32)
                cv2.fillPoly(masks[c], xy, 255)
            yield masks, image
