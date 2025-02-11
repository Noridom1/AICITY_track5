import json
import os
from PIL import Image

def yolo_to_coco(input_dir, input_txt_dir,output_json_path, category):
    images = []
    annotations = []
    annotation_id = 1
    for image_id, filename in enumerate(os.listdir(input_dir), 1):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(input_dir, filename)
            label_path = os.path.join(input_txt_dir, filename.split('.')[0]+'.txt')
            with Image.open(image_path) as img:
                width, height = img.size
            
            images.append({
                "id": filename.split('.')[0],
                "width": width,
                "height": height,
                "file_name": filename,
                'image_id':filename.split('.')[0]
            })
            
            if os.path.exists(label_path):
                with open(label_path, 'r') as file:
                    for line in file:
                        parts = line.strip().split()
                        class_id, x_center, y_center, bbox_width, bbox_height = map(float, parts[:5])
                        
                        x_min = (x_center - bbox_width / 2) * width
                        y_min = (y_center - bbox_height / 2) * height
                        bbox_width *= width
                        bbox_height *= height
                        
                        annotations.append({
                            "id": annotation_id,
                            "image_id": filename.split('.')[0],
                            "category_id":  class_id,  # YOLO类别是从0开始，COCO是从1开始
                            "bbox": [x_min, y_min, bbox_width, bbox_height],
                            "area": bbox_width * bbox_height,
                            "iscrowd": 0
                        })
                        annotation_id += 1
    
    coco_format = {
        "images": images,
        "categories":category,
        "annotations": annotations
    }
    
    with open(output_json_path, 'w') as json_file:
        json.dump(coco_format, json_file,indent=4)


input_dir = './data/aicity2024_track5/stage2/images/train'
input_txt_dir= './data/aicity2024_track5/stage2/labels/train'
output_json_path = './data/aicity2024_track5/stage2/train_ann.json'
category = [
    {"id": 0,"name": "motorbike","supercategory": "motorbike"},
    {"id": 1,"name": "DHelmet","supercategory": "DHelmet"},
    {"id": 2,"name": "DNoHelmet","supercategory": "DNoHelmet"},
    {"id": 3,"name": "P1Helmet","supercategory": "P1Helmet"},
    {"id": 4,"name": "P1NoHelmet","supercategory": "P1NoHelmet"},
    {"id": 5,"name": "P2Helmet","supercategory": "P2Helmet"},
    {"id": 6,"name": "P2NoHelmet","supercategory": "P2NoHelmet"},
    {"id": 7,"name": "P0Helmet","supercategory": "P0Helmet"},
    {"id": 8,"name": "P0NoHelmet","supercategory": "P0NoHelmet"}
    ]

yolo_to_coco(input_dir, input_txt_dir,output_json_path, category)

input_dir = './data/aicity2024_track5/stage2/images/val'
input_txt_dir= './data/aicity2024_track5/stage2/labels/val'
output_json_path = './data/aicity2024_track5/stage2/val_ann.json'
yolo_to_coco(input_dir, input_txt_dir,output_json_path, category)
