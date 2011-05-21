import xml.etree.cElementTree as ElementTree
import numpy as np
import glob
import os
import cPickle as pickle


def parse(xml_filename='sun09/Annotations/out_of_context/im001.xml'):
    # Replace a malformed character with a valid one (only one in the database)
    xml_data = open(xml_filename).read().replace('', "'")
    xml = ElementTree.fromstring(xml_data)
    filename = xml.find('filename').text.strip()
    folder = xml.find('folder').text.strip()
    objs = []
    for obj in xml.findall('object'):
        polygon = []
        for x in obj.findall('polygon'):
            polygon.append(np.array([(int(pt.find('x').text),
                                      int(pt.find('y').text))
                                     for pt in x.findall('pt')]))
                
        objs.append({'name': obj.find('name').text.strip(),
                     #'id': int(obj.find('id').text.strip()),
                     'polygon_xy': polygon})
    return filename, folder, objs


def parse_all(root_dir='sun09/'):
    data = {}
    
    for folder_path in glob.glob(root_dir + 'Annotations/*'):
        if os.path.basename(folder_path) not in ('out_of_context',
                                                 'static_sun09_database'):
            continue
        for filename_path in glob.glob(folder_path + '/*'):
            try:
                filename, folder, objs = parse(filename_path)
            except Exception, e:
                print(e)
                print('Parse Error: %s' % filename_path)
                continue
            assert os.path.basename(folder_path) == folder
            data.setdefault(folder, {})[filename] = objs
    static_data = {}
    for object_path in glob.glob('%s/Annotations/static_sun_objects/*' % (root_dir)):
        try:
            filename, folder, objs = parse(filename_path)
        except Exception, e:
            print(e)
            print('Parse Error: %s' % filename_path)
            continue
        object_name = os.path.basename(object_path)
        static_data.setdefault(object_name, []).append(objs)
    return static_data, data['out_of_context'], data['static_sun09_database']
        

def main():
    if not os.path.exists('sun09.pkl'):
        static_data, out_of_context, sun09 = parse_all()
        with open('sun09.pkl', 'w') as sun09_fp:
            pickle.dump(sun09_fp, (static_data, out_of_context, sun09), -1)
    else:
        with open('sun09.pkl') as sun09_fp:
            static_data, out_of_context, sun09 = pickle.load(sun09_fp)


if __name__ == '__main__':
    main()
