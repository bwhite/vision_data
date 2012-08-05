#!/usr/bin/env python
import hadoopy
import vision_data


class Mapper(object):
    def __init__(self):
        self.flickr = vision_data.Flickr()

    def map(self, num_kvs, query):
        for num, kv in enumerate(self.flickr.image_class_meta_url(query)):
            yield kv
            if num >= num_kvs:
                break


def reducer(key, values):
    yield key, values.next()


if __name__ == "__main__":
    hadoopy.run(Mapper, reducer, jobconfs=['mapred.task.timeout=6000000'])
