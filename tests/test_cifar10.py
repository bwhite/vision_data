try:
    import unittest2 as unittest
except ImportError:
    import unittest

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cifar10(self):
        import vision_data
        d = vision_data.CIFAR10()
        d.download()
        for z, (x, y) in enumerate(d.single_image_class_boxes()):
            if z > 10:
                break
            print(x)
            print(y.shape)

if __name__ == '__main__':
    unittest.main()

