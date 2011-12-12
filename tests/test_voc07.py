try:
    import unittest2 as unittest
except ImportError:
    import unittest


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_voc07(self):
        import vision_data
        d = vision_data.VOC07()
        d.download()
        print(d.image_class_negpos_parse())

if __name__ == '__main__':
    unittest.main()

