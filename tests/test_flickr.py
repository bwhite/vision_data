try:
    import unittest2 as unittest
except ImportError:
    import unittest

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_flickr(self):
        import vision_data
        d = vision_data.Flickr()
        import pprint
        pprint.pprint(d.image_class_meta_url('pepsi logo').next())

if __name__ == '__main__':
    unittest.main()

