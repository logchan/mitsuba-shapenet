import math
import numpy as np
import argparse
import os

def get_rand(a, b):
    return np.random.random() * (b - a) + a

def rand_pos(min_elevation, max_elevation):
    dist=2.0
    azimuth_deg = np.random.random() * 360
    elevation_deg = get_rand(min_elevation, max_elevation)
    phi = (90 - elevation_deg) / 180 * math.pi
    theta = azimuth_deg / 180 * math.pi
    x = (dist * math.cos(theta) * math.sin(phi))
    y = (dist * math.sin(theta) * math.sin(phi))
    z = (dist * math.cos(phi))
    return (x, z, y)

def mkdir_safe(path):
    if (not os.path.exists(str(path))):
        os.makedirs(str(path))

def read_file(path):
    with open(path, mode='r') as f:
        return f.read()

def write_file(path, content):
    with open(path, mode='w') as f:
        f.write(content)

fixed_positions = [ [1.15470054,-1.15470054,-1.15470054],
                    [1.15470054,-1.15470054,1.15470054],
                    [1.15470054,1.15470054,1.15470054],
                    [1.15470054,1.15470054,-1.15470054],
                    [-1.15470054,1.15470054,-1.15470054],
                    [-1.15470054,1.15470054,1.15470054],
                    [-1.15470054,-1.15470054,1.15470054],
                    [-1.15470054,-1.15470054,-1.15470054]]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, help='Input directory, e.g. /data/shapenet/02828884')
    parser.add_argument('--output', type=str, required=True, help='Where to place generated and rendered files, e.g. /data/shapenet/render/02828884')
    parser.add_argument('--template', type=str, default='template.xml', help='Path to template XML file')
    parser.add_argument('--min_elevation', type=float, default=10)
    parser.add_argument('--max_elevation', type=float, default=20)
    parser.add_argument('--render_fixed', type=bool, default=True)
    parser.add_argument('--num_random', type=int, default=8)
    args = parser.parse_args()

    print(f'Elevation range is {args.min_elevation}, {args.max_elevation}')

    # create destination directories
    in_dir = args.input
    out_dir = args.output

    render_dir = f'{out_dir}/rgb'
    mkdir_safe(out_dir)
    mkdir_safe(render_dir)

    # create xml files
    template = read_file(args.template)
    sensor_start = template.find('<sensor')
    sensor_end = template.find('</sensor>') + len('</sensor>')
    sensor_template = template[sensor_start:sensor_end]
    template = template[0:sensor_start] + '##SENSORS##' + template[sensor_end:]

    models = os.listdir(in_dir)
    count = 0
    for model in models:
        count += 1
        xml = template.replace('##FILE##', f'{in_dir}/{model}/model.obj')
        model_dir = f'{render_dir}/{model}'
        model_xml_file = f'{model_dir}/rgb.xml'
        mkdir_safe(model_dir)

        sensors = []
        random_poses = [rand_pos(args.min_elevation, args.max_elevation) for _ in range(args.num_random)]
        random_poses_str = [f'{pose[0]:.16f},{pose[1]:.16f},{pose[2]:.16f}' for pose in random_poses]

        if args.render_fixed:
            all_poses = [*fixed_positions, *random_poses]
        else:
            all_poses = random_poses

        for pose_id in range(len(all_poses)):
            pose = all_poses[pose_id]
            pose = f'{pose[0]:.16f},{pose[1]:.16f},{pose[2]:.16f}'
            sensors.append(sensor_template.replace('##ORIGIN##', pose))
        
        write_file(f'{model_dir}/random_poses.txt', '\n'.join(random_poses_str) + '\n')
        write_file(model_xml_file, xml.replace('##SENSORS##', '\n'.join(sensors) + '\n'))
