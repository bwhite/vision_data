#!/usr/bin/env python
import urllib2
import socket
import hadoopy
import os


def download_file(url):
    num_attempts = 3
    socket.setdefaulttimeout(3)
    for attempt in range(num_attempts):
        try:
            data = urllib2.urlopen(url).read()
            break
        except Exception, e:
            if attempt == (num_attempts - 1):  # If last attempt
                raise e
    return data


class Mapper(object):

    def __init__(self):
        self.output_type = os.environ.get('OUTPUT_TYPE', 'image')

    def map(self, url, value):
        try:
            data = download_file(url)
        except Exception:
            hadoopy.counter('FILE_DOWNLOADER', 'Exception')
        else:
            if self.output_type == 'meta':
                yield url, (data, value)
            elif self.output_type == 'image':
                yield url, data
            else:
                raise ValueError('OutputType[%s]' % self.output_type)


if __name__ == "__main__":
    hadoopy.run(Mapper)
