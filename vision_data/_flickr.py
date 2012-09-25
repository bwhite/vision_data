#!/usr/bin/env python
import time
import random
import xml.parsers.expat
import urllib2
import httplib
import vision_data
import os
import xml.etree.ElementTree
import sys


class Flickr(vision_data.VisionDataset):
    """
    """

    def __init__(self, max_iters=10, max_pages=1):
        super(Flickr, self).__init__(name='flickr',
                                     homepage='http://www.flickr.com',
                                     bibtexs=None,
                                     overview=None,
                                     no_root=True)
        import flickrapi
        api_key = ''  # NOTE(brandyn): Include your flickr api key and secret here
        api_secret = ''
        try:
            from flickr_api_key import api_key, api_secret
        except ImportError:
            api_key = os.environ.get('FLICKR_API_KEY')
            api_secret = os.environ.get('FLICKR_API_SECRET')
            if not api_key or not api_secret:
                print('Missing flickr API key')
                import sys
                sys.exit(1)
        self.api_key = api_key
        self.api_secret = api_secret
        self.earliest = 1167631200
        self.date_radius = 15552000  # 6 months
        self.per_page = 500
        self.has_geo = 'HAS_GEO' in os.environ
        self.sleep_penalty_max = 30
        self.sleep_penalty = 5
        self.sleep_penalty_orig = 5
        self.extras = 'description,license,date_upload,date_taken,owner_name,icon_server,original_format,last_update,geo,tags,machine_tags,o_dims,views,media,path_alias,url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
        self.flickr = flickrapi.FlickrAPI(self.api_key)
        self.min_rnd_date = self.earliest + self.date_radius
        self.max_rnd_date = int(time.time()) - self.date_radius
        self.max_pages = max_pages
        self.max_iters = max_iters

    def _query(self, value, dates=None, page=None):
        import flickrapi
        try:
            kw = {}
            if dates:
                kw['min_upload_date'] = dates[0]
                kw['max_upload_date'] = dates[1]
            if page:
                kw['page'] = page
            if self.has_geo:
                kw['has_geo'] = 1
            return self.flickr.photos_search(text=value,
                                             extras=self.extras,
                                             per_page=self.per_page,
                                             **kw)
            self.sleep_penalty = self.sleep_penalty_orig
        except (httplib.BadStatusLine,
                flickrapi.exceptions.FlickrError,
                xml.parsers.expat.ExpatError,
                xml.etree.ElementTree.ParseError,
                urllib2.URLError,
                urllib2.HTTPError), e:
            sys.stderr.write('Except[%s]\n' % str(e))
            time.sleep(self.sleep_penalty)
            self.sleep_penalty = min(self.sleep_penalty_max, self.sleep_penalty * 2)

    def _get_data(self, res):
        if res:
            for photo in res.find('photos'):
                photo = dict(photo.items())
                try:
                    yield photo['url_m'], photo
                except KeyError:
                    return

    def image_class_meta_url(self, value):
        """
        Args:
            tags:

        Returns:
            Data is in the form of (image_url, metadata)
        """
        for page in range(1, self.max_pages):
            for k, v in self._get_data(self._query(value, page=page)):
                yield k, v
        cur_iter = 0
        while 1:
            if cur_iter >= self.max_iters:
                break
            sys.stderr.write('Iter[%d][%s]\n' % (cur_iter, value))
            cur_iter += 1
            cur_time_center = random.randint(self.min_rnd_date, self.max_rnd_date)
            min_date = cur_time_center - self.date_radius
            max_date = cur_time_center + self.date_radius
            for k, v in self._get_data(self._query(value, (min_date, max_date))):
                yield k, v
