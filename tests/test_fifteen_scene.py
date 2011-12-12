try:
    import unittest2 as unittest
except ImportError:
    import unittest


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fifteen_scene(self):
        import vision_data
        d = vision_data.FifteenScene()
        d.download()
        scenes = d.scene_rec_parse()
        print(scenes)

if __name__ == '__main__':
    unittest.main()

