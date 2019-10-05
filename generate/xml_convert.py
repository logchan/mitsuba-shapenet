import math
import numpy as np
import argparse
import os
from pathlib import Path

def get_rand(a, b):
    return np.random.random() * (b - a) + a

def update_pos(pose, min_elevation, max_elevation):
    dist = 2.0

    pose = pose.split(',')
    x, z, y = [float(p) for p in pose]
    new_elev = get_rand(min_elevation, max_elevation)
    print(f'Old elevation is {90 - math.acos(z / dist) * 180 / math.pi}')
    print(f'New elevation is {new_elev}')
    r = math.sqrt(x*x + y*y)
    z = r * math.tan(new_elev / 180 * math.pi)

    l = math.sqrt(x*x + y*y + z*z)
    x *= dist/l
    y *= dist/l
    z *= dist/l

    # sanity check
    print('Length err:', x*x+y*y+z*z-dist*dist)
    x0, _, y0 = [float(p) for p in pose]
    print('xy ratio', x/x0)
    print('Proj err:', y-x/x0*y0)
    print(f'Elev est.: {90 - math.acos(z / dist) * 180 / math.pi}')
    return f'{x:.16f},{z:.16f},{y:.16f}'

def read_file(path):
    with open(path, mode='r') as f:
        return f.read()

def read_first_line(path):
    with open(path, mode='r') as f:
        return f.readline()

def write_file(path, content):
    with open(path, mode='w') as f:
        f.write(content)

parser = argparse.ArgumentParser()
parser.add_argument('--model_dir', type=str, required=True, help='Where are ShapeNet models, e.g. /data/shapenet')
parser.add_argument('--input', type=str, required=True, help='Input directory, e.g. /data/shapenet/render')
parser.add_argument('--output', type=str, required=True, help='Where to place generated and rendered files, e.g. /data/shapenet/render2')
parser.add_argument('--template', type=str, default='template.xml', help='Path to template XML file')
parser.add_argument('--min_elevation', type=float, default=25)
parser.add_argument('--max_elevation', type=float, default=30)
args = parser.parse_args()

args.model_dir = Path(args.model_dir)
args.input = Path(args.input)
args.output = Path(args.output)

template = read_file(args.template)
sensor_start = template.find('<sensor')
sensor_end = template.find('</sensor>') + len('</sensor>')
sensor_template = template[sensor_start:sensor_end]
template = template[0:sensor_start] + '##SENSORS##' + template[sensor_end:]

names = []
for cl in os.listdir(args.input):
    for name in os.listdir(args.input / cl / 'rgb'):
        names.append(f'{cl}/rgb/{name}')
print(len(names))

for name in names:
    print(f'Convert {name}')
    pose = read_first_line(args.input / name / 'random_poses.txt').rstrip('\n')
    print(f'Original pose: {pose}')
    pose = update_pos(pose, args.min_elevation, args.max_elevation)
    print(f'Converted pose: {pose}')

    xml = template.replace('##FILE##', str(args.model_dir / name.replace('rgb/', '') / 'model.obj'))
    sensor = sensor_template.replace('##ORIGIN##', pose)
    xml = xml.replace('##SENSORS##', sensor + '\n')

    model_dir = args.output / name
    os.makedirs(model_dir, exist_ok=True)

    write_file(model_dir / 'random_poses.txt', pose + '\n')
    write_file(model_dir / 'rgb.xml', xml)