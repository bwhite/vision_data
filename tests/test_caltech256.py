try:
    import unittest2 as unittest
except ImportError:
    import unittest

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_caltech256(self):
        import vision_data
        data = vision_data.Caltech256()
        data.download()
        print(data.image_class_parse())

if __name__ == '__main__':
    unittest.main()

