import xml.etree.ElementTree as ET
import os


def parse_annotation(train_path, ann_dir, img_dir, labels=[], x_ratio =1, y_ratio = 1):
    all_imgs = []
    seen_labels = {}
    
    f = open(train_path,'r')
    content = f.readlines()
    for cont in content:
        img_name = cont.strip()
#     for ann in sorted(os.listdir(ann_dir)):
        img = {'object':[]}

#         tree = ET.parse(ann_dir + ann)
        tree = ET.parse(os.path.join(ann_dir, img_name +'.xml'))
    
        for elem in tree.iter():
            if 'filename' in elem.tag:
#                 img['filename'] = img_dir + elem.text
                img['filename']= img_name +'.jpg'
            if 'width' in elem.tag:
                img['width'] = int(elem.text)
            if 'height' in elem.tag:
                img['height'] = int(elem.text)
            if 'object' in elem.tag or 'part' in elem.tag:
                obj = {}
                
                for attr in list(elem):
                    if 'name' in attr.tag:
                        obj['name'] = attr.text

                        if obj['name'] in seen_labels:
                            seen_labels[obj['name']] += 1
                        else:
                            seen_labels[obj['name']] = 1
                        
                        if len(labels) > 0 and obj['name'] not in labels:
                            break
                        else:
                            img['object'] += [obj]
                            
                    if 'bndbox' in attr.tag:
                        for dim in list(attr):
                            if 'xmin' in dim.tag:
                                obj['xmin'] = int(round(float(dim.text))*x_ratio)
                            if 'ymin' in dim.tag:
                                obj['ymin'] = int(round(float(dim.text))*y_ratio)
                            if 'xmax' in dim.tag:
                                obj['xmax'] = int(round(float(dim.text))*x_ratio)
                            if 'ymax' in dim.tag:
                                obj['ymax'] = int(round(float(dim.text))*y_ratio)

        if len(img['object']) > 0:
            all_imgs += [img]
                        
    return all_imgs, seen_labels

base_path = '/Ted/datasets/Garbage'
folders = ['VOC_Test_Easy','VOC_Test_Hard']
split = 'test' #can be train, train_val or test

LABELS = ['garbage'] # array containing labels. Can be more than one.
for folder in folders:
    train_image_folder = os.path.join(base_path,folder,'JPEGImages')
    train_annot_folder = os.path.join(base_path,folder,'Annotations')
    train_file_path = os.path.join(base_path,folder,'ImageSets/Main',split + '.txt')
    save_dir = os.path.join(base_path,folder,'ground-truths')
    train_imgs, seen_train_labels = parse_annotation(train_file_path, train_annot_folder, train_image_folder, labels=LABELS,)

    #label_ids = seen_train_labels.copy()
    labels_ids = {'garbage': 'garbage'}
    f = open(train_file_path,'r')
    lines = f.readlines()
    count = 0
    for line in lines:
        if count == len(train_imgs):
            break
        img_name = line.strip()
        xml_text = open(os.path.join(save_dir,img_name + '.txt'),'w+')
        
        image = train_imgs[count]
        count +=1
        im_name = image['filename'].split('/')[-1]
        objects = image['object']
        # print (im_name)
    #     line = im_name
        for objs in objects:
            xmin = objs['xmin']
            ymin = objs['ymin']
            xmax = objs['xmax']
            ymax = objs['ymax']
            c_id = labels_ids[objs['name']]
    #         print (xmin, ymin, xmax, ymax, c_id)
            line = str(c_id) +' '+str(xmin)+' ' +str(ymin)+' ' +str(xmax)+' '+str(ymax)+' ' +'\n'
            xml_text.write (line)
        
        xml_text.close()
#  print (line)
        
    f.close()



