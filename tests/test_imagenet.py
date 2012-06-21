try:
    import unittest2 as unittest
except ImportError:
    import unittest


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_imagenet(self):
        import vision_data
        d = vision_data.ImageNet()
        #d.download2()
        d.object_rec_parse()

if __name__ == '__main__':
    unittest.main()

