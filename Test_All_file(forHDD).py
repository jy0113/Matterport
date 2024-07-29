import os
import json
import csv

def parse_o_line(line):
    fields = line.strip().split()
    object_type = fields[0]
    object_index = int(fields[1])
    region_index = int(fields[2])
    category_index = int(fields[3])
    px, py, pz = map(float, fields[4:7])
    a0x, a0y, a0z = map(float, fields[7:10])
    a1x, a1y, a1z = map(float, fields[10:13])
    r0, r1, r2 = map(float, fields[13:16])
    additional_values = list(map(float, fields[16:]))
    
    obj = {
        "object_type": object_type,
        "object_index": object_index,
        "region_index": region_index,
        "category_index": category_index,
        "position": [px, py, pz],
        "axis_directions(a0)": [a0x, a0y, a0z],
        "axis_directions(a1)": [a1x, a1y, a1z],
        "radii(r)": [r0, r1, r2],
        "additional_values": additional_values,
        "category_details": None,
        "segments": []
    }
    return obj

def parse_c_line(line):
    fields = line.strip().split()
    category_index = int(fields[1])
    category_mapping_index = int(fields[2])
    category_mapping_name = fields[3]
    mpcat40_index = int(fields[4])
    mpcat40_name = fields[5]
    
    category = {
        "category_index": category_index,
        "category_mapping_index": category_mapping_index,
        "category_mapping_name": category_mapping_name,
        "mpcat40_index": mpcat40_index,
        "mpcat40_name": mpcat40_name
    }
    return category

def parse_e_line(line):
    fields = line.strip().split()
    segment_index = int(fields[1])
    object_index = int(fields[2])
    segment_id = int(fields[3])
    area = float(fields[4])
    px, py, pz = map(float, fields[5:8])
    xlo, ylo, zlo = map(float, fields[8:11])
    xhi, yhi, zhi = map(float, fields[11:14])
    
    segment = {
        "segment_index": segment_index,
        "object_index": object_index,
        "segment_id": segment_id,
        "area": area,
        "position": [px, py, pz],
        "bbox": [xlo, ylo, zlo, xhi, yhi, zhi]
    }
    return segment

def parse_p_portal_line(line):
    fields = line.strip().split()
    portal_index = int(fields[1])
    region0_index = int(fields[2])
    region1_index = int(fields[3])
    label = fields[4]
    xlo, ylo, zlo = map(float, fields[5:8])
    xhi, yhi, zhi = map(float, fields[8:11])
    
    portal = {
        "portal_index": portal_index,
        "regions": [region0_index, region1_index],
        "label": label,
        "bbox": [xlo, ylo, zlo, xhi, yhi, zhi]
    }
    return portal

def parse_p_panorama_line(line):
    fields = line.strip().split()
    name = fields[1]
    panorama_index = int(fields[2])
    region_index = int(fields[3])
    px, py, pz = map(float, fields[5:8])
    
    panorama = {
        "name": name,
        "panorama_index": panorama_index,
        "region_index": region_index,
        "position": [px, py, pz],
        "images": []
    }
    return panorama

def parse_i_line(line):
    fields = line.strip().split()
    image_index = int(fields[1])
    panorama_index = int(fields[2])
    name = fields[3]
    camera_index = int(fields[4])
    yaw_index = int(fields[5])
    e = list(map(float, fields[6:22]))
    i = list(map(float, fields[22:31]))
    width = int(fields[31])
    height = int(fields[32])
    px, py, pz = map(float, fields[33:36])
    
    image = {
        "image_index": image_index,
        "panorama_index": panorama_index,
        "name": name,
        "camera_index": camera_index,
        "yaw_index": yaw_index,
        "extrinsics": e,
        "intrinsics": i,
        "width": width,
        "height": height,
        "position": [px, py, pz]
    }
    return image

def parse_r_line(line):
    fields = line.strip().split()
    region_index = int(fields[1])
    level_index = int(fields[2])
    label = fields[5]
    px, py, pz = map(float, fields[6:9])
    xlo, ylo, zlo = map(float, fields[9:12])
    xhi, yhi, zhi = map(float, fields[12:15])
    height = float(fields[15])
    
    room = {
        "region_index": region_index,
        "level_index": level_index,
        "label": label,
        "position": [px, py, pz],
        "bbox": [xlo, ylo, zlo, xhi, yhi, zhi],
        "height": height,
        "objects": [],
        "portals": []
    }
    return room

def parse_l_line(line):
    fields = line.strip().split()
    level_index = int(fields[1])
    num_regions = int(fields[2])
    label = fields[3]
    px, py, pz = map(float, fields[4:7])
    xlo, ylo, zlo = map(float, fields[7:10])
    xhi, yhi, zhi = map(float, fields[10:13])
    
    level = {
        "level_index": level_index,
        "num_regions": num_regions,
        "label": label,
        "position": [px, py, pz],
        "bbox": [xlo, ylo, zlo, xhi, yhi, zhi]
    }
    return level

def parse_h_line(line):
    fields = line.strip().split()
    name = fields[1]
    label = fields[2]
    px, py, pz = map(float, fields[10:13])
    xlo, ylo, zlo = map(float, fields[13:16])
    xhi, yhi, zhi = map(float, fields[16:19])
    
    building = {
        "name": name,
        "label": label,
        "position": [px, py, pz],
        "bbox": [xlo, ylo, zlo, xhi, yhi, zhi]
    }
    return building

def read_tsv_file(tsv_file_path):
    tsv_data = {}
    with open(tsv_file_path, 'r', encoding='utf-8') as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        for row in reader:
            index = int(row['index']) if row['index'] else None
            if index is not None:
                tsv_data[index] = {
                    "category": row['category'] if row['category'] else None,
                    "count": int(row['count']) if row['count'] else None,
                    "nyuId": int(row['nyuId']) if row['nyuId'] else None,
                    "nyu40id": int(row['nyu40id']) if row['nyu40id'] else None,
                    "nyuClass": row['nyuClass'] if row['nyuClass'] else None,
                    "nyu40class": row['nyu40class'] if row['nyu40class'] else None
                }
    return tsv_data


def read_o_c_e_p_r_l_h_sections(file_path):
    objects = {}
    categories = {}
    portals = []
    panoramas = []
    rooms = {}
    levels = []
    building = None
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("O "):
                obj = parse_o_line(line)
                objects[obj["object_index"]] = obj
            elif line.startswith("C "):
                category = parse_c_line(line)
                categories[category["category_index"]] = category
            elif line.startswith("E "):
                segment = parse_e_line(line)
                if segment["object_index"] in objects:
                    objects[segment["object_index"]]["segments"].append(segment)
            elif line.startswith("R "):
                room = parse_r_line(line)
                rooms[room["region_index"]] = room
            elif line.startswith("P "):
                fields = line.strip().split()
                if len(fields) == 15:  # Check if it's a portal line based on the number of fields
                    portal = parse_p_portal_line(line)
                    portals.append(portal)
                else:  # panorama line
                    panorama = parse_p_panorama_line(line)
                    panoramas.append(panorama)
            elif line.startswith("I "):
                image = parse_i_line(line)
                for panorama in panoramas:
                    if panorama["panorama_index"] == image["panorama_index"]:
                        panorama["images"].append(image)
                        break
            elif line.startswith("L "):
                level = parse_l_line(line)
                levels.append(level)
            elif line.startswith("H "):
                building = parse_h_line(line)
            #Use capital letter to distinguish
    for obj in objects.values():
        category_index = obj["category_index"]
        if category_index in categories:
            obj["category_details"] = categories[category_index]

    for obj in objects.values():
        if obj["region_index"] in rooms:
            rooms[obj["region_index"]]["objects"].append(obj)

    for portal in portals:
        for region_index in portal["regions"]:
            if region_index in rooms:
                rooms[region_index]["portals"].append(portal)

    return {"rooms": list(rooms.values()), "levels": levels, "building": building, "panoramas": panoramas, "categories": categories}

def merge_objects_with_categories(data, tsv_data):
    rooms = data["rooms"]
    categories = data["categories"]
    for room in rooms:
        for obj in room["objects"]:
            category_index = obj["category_index"]
            if category_index in categories:
                category_details = categories[category_index]
                mapping_index = category_details["category_mapping_index"]
                if mapping_index in tsv_data:
                    category_details.update(tsv_data[mapping_index])
                obj["category_details"] = category_details
    return rooms

def save_to_json(data, output_file):
    output_data = {
        "building": data["building"],
        "levels": data["levels"],
        "rooms": data["rooms"],
        "panoramas": data["panoramas"]
    }
    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent=4)

def process_id_file(id_file, root_directory, tsv_file, output_directory):
    with open(id_file, 'r') as file:
        ids = [line.strip() for line in file.readlines()]
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    tsv_data = read_tsv_file(tsv_file)
    for id_ in ids:
        input_file = os.path.join(root_directory, id_, id_, 'house_segmentations', f'{id_}.house')
        output_file = os.path.join(output_directory, f'{id_}.json')
        if os.path.exists(input_file):
            data = read_o_c_e_p_r_l_h_sections(input_file)
            data["rooms"] = merge_objects_with_categories(data, tsv_data)
            save_to_json(data, output_file)
            print(f'Processed {input_file}, output saved to {output_file}')
        else:
            print(f'Input file {input_file} does not exist.')

root_directory = '.'  
id_file = 'ID.txt'  
tsv_file = 'category_mapping.tsv'  
output_directory = './output'  

process_id_file(id_file, root_directory, tsv_file, output_directory)
