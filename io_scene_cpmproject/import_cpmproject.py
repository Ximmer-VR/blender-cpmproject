import os
import zipfile
import json
import bpy
import math
from mathutils import Euler, Vector
import tempfile

alex_model = {
    'head': {
        'pos': [0, 0, 0],
        'size': [8, 8, 8],
        'offset': [0, -4, 0],
        'uv': {'x': 0, 'y': 0},
    },
    'body': {
        'pos': [0, 0, 0],
        'size': [8, 12, 4],
        'offset': [0, 6, 0],
        'uv': {'x': 16, 'y': 16},
    },
    'right_arm': {
        'pos': [-5, 2, 0],
        'size': [3, 12, 4],
        'offset': [-0.5, 4, 0],
        'uv': {'x': 5*8, 'y': 2*8},
    },
    'left_arm': {
        'pos': [5, 2, 0],
        'size': [3, 12, 4],
        'offset': [0.5, 4, 0],
        'uv': {'x': 32, 'y': 48},
    },
    'right_leg': {
        'pos': [-2, 12, 0],
        'size': [4, 12, 4],
        'offset': [0, 6, 0],
        'uv': {'x': 0, 'y': 16},
    },
    'left_leg': {
        'pos': [2, 12, 0],
        'size': [4, 12, 4],
        'offset': [0, 6, 0],
        'uv': {'x': 16, 'y': 48},
    },
}

def vec3_div(vec3, num):
    return [vec3[0] / num, vec3[1] / num, vec3[2] / num]

def vec3_add(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]

def vec3_sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

def vec3_zy(a):
    return [a[0], a[2], -a[1]]

def add_cube(pos, offset, rot, size, scale, name, voxel=True):

    pos = vec3_zy(pos)
    offset = vec3_zy(offset)
    size = vec3_zy(size)
    size[2] = -size[2]
    size[0] = size[0] + scale
    size[1] = size[1] + scale
    size[2] = size[2] + scale
    rot = vec3_zy(rot)

    # e = Euler(rot, 'XYZ')
    # offset = e.to_matrix() @ Vector((offset[0], offset[1], offset[2]))

    if scale == 0:
        if size[0] == 0:
            size[0] = 0.001
        if size[1] == 0:
            size[1] = 0.001
        if size[2] == 0:
            size[2] = 0.001

    bpy.ops.mesh.primitive_cube_add(size=1.0)
    cube = bpy.context.active_object

    if voxel:
        cube.location = [0.5, 0.5, -0.5]
        bpy.ops.object.transform_apply(location=True)

    cube.location = vec3_sub(vec3_add(pos, offset), [scale / 2.0, scale / 2.0, -scale / 2.0])
    cube.scale = size
    bpy.ops.object.transform_apply(scale=True)

    cube.name = name

    bpy.context.scene.cursor.location = pos
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    rot = (math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]))

    cube.rotation_euler = Euler(rot, 'XYZ')

    return cube

def auto_arrange_nodes(node_tree):
    nodes = node_tree.nodes

    x = -200
    y = 0

    for node in nodes:
        node.location.x = x
        node.location.y = y
        x += 400

def process_faceuv(cube, faceUV, skin_size):
    mesh = cube.data
    uv_layer = mesh.uv_layers.active.data

    order = [
        'west',
        'south',
        'east',
        'north',
        'down',
        'up',
    ]

    rotations = [
        0,0,0,0,
        1,3
    ]

    for i, face in enumerate(mesh.polygons):
        if i >= len(order):
            break

        if order[i] not in faceUV:
            continue

        k = face.loop_start

        uv_data = faceUV[order[i]]

        rot = int(int(uv_data['rot']) / 90) + rotations[i]

        uv_layer[k + (0 + rot) % 4].uv[0:2] = uv_data['ex'] / skin_size[0], 1 - uv_data['ey'] / skin_size[1]
        uv_layer[k + (1 + rot) % 4].uv[0:2] = uv_data['ex'] / skin_size[0], 1 - uv_data['sy'] / skin_size[1]
        uv_layer[k + (2 + rot) % 4].uv[0:2] = uv_data['sx'] / skin_size[0], 1 - uv_data['sy'] / skin_size[1]
        uv_layer[k + (3 + rot) % 4].uv[0:2] = uv_data['sx'] / skin_size[0], 1 - uv_data['ey'] / skin_size[1]

def process_uv(cube, uv, size, skinSize, mirror):
    mesh = cube.data
    uv_layer = mesh.uv_layers.active.data

    sx, sy, sz = size

    if mirror:
        index2offset = [
            [sz+sx+sz,    sz, -sz, sy, 0],  # left
            [sz+sx+sz+sx, sz, -sx, sy, 0],  # back
            [0+sz,        sz, -sz, sy, 0],  # right
            [sz+sx,       sz, -sx, sy, 0],  # front

            [sz+sx, 0, sx, sz, 1],      # bottom
            [sz,    0, sx, sz, 1],      # top
        ]
    else:
        index2offset = [
            [0,        sz, sz, sy, 0],  # right
            [sz+sx+sz, sz, sx, sy, 0],  # back
            [sz+sx,    sz, sz, sy, 0],  # left
            [sz,       sz, sx, sy, 0],  # front

            [sz+sx, 0, sx, sz, 3],      # bottom
            [sz,    0, sx, sz, 3],      # top
        ]

    for i, face in enumerate(mesh.polygons):
        x, y, w, h, rot = index2offset[i]

        k = face.loop_start

        uv_layer[k + (0 + rot) % 4].uv[0:2] = (uv[0] + w + x) / skinSize[0], 1 - (uv[1] + h + y) / skinSize[1]
        uv_layer[k + (1 + rot) % 4].uv[0:2] = (uv[0] + w + x) / skinSize[0], 1 - (uv[1] + 0 + y) / skinSize[1]
        uv_layer[k + (2 + rot) % 4].uv[0:2] = (uv[0] + 0 + x) / skinSize[0], 1 - (uv[1] + 0 + y) / skinSize[1]
        uv_layer[k + (3 + rot) % 4].uv[0:2] = (uv[0] + 0 + x) / skinSize[0], 1 - (uv[1] + h + y) / skinSize[1]

def load(context,
         filepath,
         import_uvs = True,               # import face uvs
         import_textures = True,          # import textures into materials
         recenter_to_origin = True,       # recenter model to origin, overrides translate origin
         **kwargs):
    """Main import function"""

    with zipfile.ZipFile(filepath) as zip_file:
        if 'config.json' not in zip_file.namelist():
            print('config.json not found in cpmproject')
            return {"CANCELLED"}

        material = None

        # textures
        if 'skin.png' in zip_file.namelist():
            texture_data = zip_file.read("skin.png")

            temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            temp_file.write(texture_data)
            temp_file.flush()
            temp_file.close()

            image = bpy.data.images.load(temp_file.name)
            bpy.context.view_layer.update()
            image.name = 'skin.png'

            material = bpy.data.materials.new(name="skin")
            material.blend_method = 'CLIP'
            material.use_nodes = True
            tree = material.node_tree
            nodes = tree.nodes

            for node in nodes:
                nodes.remove(node)

            image_texture_node = nodes.new(type='ShaderNodeTexImage')
            image_texture_node.image = image
            image_texture_node.interpolation = 'Closest'

            diffuse_node = nodes.new(type='ShaderNodeBsdfPrincipled')
            diffuse_node.inputs['Roughness'].default_value = 1.0

            material_output_node = nodes.new(type='ShaderNodeOutputMaterial')

            links = tree.links

            links.new(image_texture_node.outputs['Color'], diffuse_node.inputs['Base Color'])
            links.new(image_texture_node.outputs['Alpha'], diffuse_node.inputs['Alpha'])
            links.new(diffuse_node.outputs['BSDF'], material_output_node.inputs['Surface'])

            auto_arrange_nodes(tree)


        # geometry
        with zip_file.open('config.json') as json_file:
            data = json.load(json_file)

        if not 'elements' in data:
            print('data missing elements')
            return {"CANCELLED"}

        objects = []

        skin_size = [data['skinSize']['x'], data['skinSize']['y']]

        for element in data['elements']:
            #print('{}'.format(element['id']))
            cube = None
            pos = [0,0,0]
            pos = [0,0,0]

            if element['id'] in alex_model:
                default = alex_model[element['id']]
                pos = default['pos']
                pos = vec3_add(pos, [0, -24, 0])
                if 'pos' in element:
                    element_pos = [element['pos']['x'], element['pos']['y'], element['pos']['z']]
                    pos = vec3_add(pos, element_pos)
                offset = default['offset']
                size = default['size']

                cube = add_cube(pos, offset, [0,0,0], size, 0, element['id'], False)

                if 'uv' in default:
                    uv = [default['uv']['x'], default['uv']['y']]
                    process_uv(cube, uv, size, [64,64], False)

                if material is not None:
                    cube.data.materials.append(material)

                if 'show' in element and element['show'] == False:
                    cube.hide_set(True)

                if 'children' in element:
                    child_objects = process_children(element['children'], cube, pos, [0,0,0], material, skin_size)

                    objects.extend(child_objects)


    return {"FINISHED"}

def parent_without_movement(child_obj, parent_obj):
    child_obj.parent = parent_obj

def process_children(children, parent, core_pos, rot, material, skin_size):
    objects = []
    for child in children:

        pos = child['pos']['x'], child['pos']['y'], child['pos']['z']
        #pos = vec3_add(pos, core_pos)
        offset = [child['offset']['x'], child['offset']['y'], child['offset']['z']]
        rot_euler = (child['rotation']['x'], child['rotation']['y'], child['rotation']['z'])
        size = [child['size']['x'], child['size']['y'], child['size']['z']]
        uv = [child['u'], child['v']]
        mirror = child['mirror']
        mcScale = child['mcScale']

        cube = add_cube(pos, offset, rot_euler, size, mcScale, child['name'])

        process_uv(cube, uv, size, skin_size, mirror)
        if 'faceUV' in child:
            process_faceuv(cube, child['faceUV'], skin_size)

        if material is not None:
            cube.data.materials.append(material)

        parent_without_movement(cube, parent)

        if 'show' in child and child['show'] == False:
            cube.hide_set(True)

        if 'children' in child:
            child_objects = process_children(child['children'], cube, pos, vec3_add(rot, rot_euler), material, skin_size)

            objects.extend(child_objects)

        objects.append(cube)

    return objects
