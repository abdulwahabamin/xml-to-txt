import xml.etree.ElementTree as ET
import os
import cv2
import argparse


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str)
    parser.add_argument('--pred_dir', type=str)
    parser.add_argument('--save_dir', type=str)
    return parser.parse_args()


def main():
    input_args = _parse_args()
    images_pred = [k for k in os.listdir(input_args.pred_dir) if '.txt' in k]
    for pred in images_pred:
        image_name = pred.split('.txt')[0]
        image_path = os.path.join(input_args.image_dir, image_name + '.jpg')
        prediction_path = os.path.join(input_args.pred_dir, pred)
        annotation = ET.Element('annotation')
        folder = ET.SubElement(annotation, 'folder')
        folder.text = 'pi_data_2'
        filename = ET.SubElement(annotation, 'filename')
        filename.text = image_name + '.jpg'
        path = ET.SubElement(annotation, 'path')
        path.text = image_path
        source = ET.SubElement(annotation, 'source')
        database = ET.SubElement(source, 'database')
        database.text = 'Unknown'
        size = ET.SubElement(annotation, 'size')
        image = cv2.imread(image_path)
        w, h, d = image.shape
        width = ET.SubElement(size, 'width')
        height = ET.SubElement(size, 'height')
        depth = ET.SubElement(size, 'depth')
        height.text = str(w)
        width.text = str(h)
        depth.text = str(d)
        segmented = ET.SubElement(annotation, 'segmented')
        segmented.text = '0'
        f = open(prediction_path, 'r')
        lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line == '':
                break
            prediction = line.split(' ')
            object_ = ET.SubElement(annotation, 'object')
            name = ET.SubElement(object_, 'name')
            pose = ET.SubElement(object_, 'pose')
            truncated = ET.SubElement(object_, 'truncated')
            difficult = ET.SubElement(object_, 'difficult')
            bndbox = ET.SubElement(object_, 'bndbox')
            xmin = ET.SubElement(bndbox, 'xmin')
            ymin = ET.SubElement(bndbox, 'ymin')
            xmax = ET.SubElement(bndbox, 'xmax')
            ymax = ET.SubElement(bndbox, 'ymax')

            name.text = str(prediction[0])
            pose.text = 'Unspecified'
            truncated.text = '0'
            difficult.text = '0'
            xmin.text = str(prediction[2])
            ymin.text = str(prediction[3])
            xmax.text = str(prediction[4])
            ymax.text = str(prediction[5])

        # create a new XML file with the results
        mydata = ET.tostring(annotation, encoding='unicode')
        myfile = open(os.path.join(input_args.save_dir, f'{image_name}.xml'), 'w+')
        myfile.write(mydata)


if __name__ == '__main__':
    main()