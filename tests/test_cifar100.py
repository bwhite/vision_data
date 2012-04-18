try:
    import unittest2 as unittest
except ImportError:
    import unittest

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cifar100(self):
        import vision_data
        d = vision_data.CIFAR100()
        d.download()
        #out = d.image_class_parse()
        #print(out.items()[:10])

if __name__ == '__main__':
    unittest.main()

