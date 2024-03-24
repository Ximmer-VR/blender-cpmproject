import zipfile
import json
import bpy
import tempfile
import shutil
import math

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

data_template = {
  "removeBedOffset": False,
  "scaling": 0.0,
  "skinType": "slim",
  "textures": {
    "skin": {
      "customGridSize": False,
      "anim": []
    }
  },
  "enableInvisGlow": False,
  "hideHeadIfSkull": True,
  "elements": [
    {
      "disableVanillaAnim": False,
      "pos": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "nameColor": 0,
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "show": True,
      "name": "",
      "id": "head",
      "locked": False,
      "showInEditor": True,
      "dup": False
    },
    {
      "disableVanillaAnim": False,
      "pos": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "nameColor": 0,
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "show": True,
      "name": "",
      "id": "body",
      "locked": False,
      "showInEditor": True,
      "dup": False
    },
    {
      "disableVanillaAnim": False,
      "pos": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "nameColor": 0,
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "show": True,
      "name": "",
      "id": "left_arm",
      "locked": False,
      "showInEditor": True,
      "dup": False
    },
    {
      "disableVanillaAnim": False,
      "pos": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "nameColor": 0,
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "show": True,
      "name": "",
      "id": "right_arm",
      "locked": False,
      "showInEditor": True,
      "dup": False
    },
    {
      "disableVanillaAnim": False,
      "pos": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "nameColor": 0,
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "show": True,
      "name": "",
      "id": "left_leg",
      "locked": False,
      "showInEditor": True,
      "dup": False
    },
    {
      "disableVanillaAnim": False,
      "pos": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "nameColor": 0,
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "show": True,
      "name": "",
      "id": "right_leg",
      "locked": False,
      "showInEditor": True,
      "dup": False
    }
  ],
  "skinSize": {
    "x": 64,
    "y": 64
  },
  "version": 1,
  "removeArmorOffset": True,
  "scalingEx": {
    "mining_speed": 1.0,
    "hitbox_width": 1.0,
    "reach": 1.0,
    "attack_speed": 1.0,
    "jump_height": 1.0,
    "render_rotation": {
      "x": 0.0,
      "y": 0.0,
      "z": 0.0
    },
    "step_height": 1.0,
    "attack_knockback": 1.0,
    "defense": 1.0,
    "hitbox_height": 1.0,
    "fall_damage": 1.0,
    "attack_dmg": 1.0,
    "height": 1.0,
    "projectile_dmg": 1.0,
    "eye_height": 1.0,
    "third_person": 1.0,
    "motion": 1.0,
    "flight_speed": 1.0,
    "mob_visibility": 1.0,
    "knockback_resist": 1.0,
    "health": 1.0,
    "view_bobbing": 1.0,
    "explosion_dmg": 1.0,
    "safe_fall_distance": 1.0,
    "width": 1.0,
    "render_scale": {
      "x": 0.0,
      "y": 0.0,
      "z": 0.0
    },
    "render_position": {
      "x": 0.0,
      "y": 0.0,
      "z": 0.0
    }
  },
  "firstPersonHand": {
    "left": {
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "scale": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "position": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      }
    },
    "right": {
      "rotation": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "scale": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "position": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      }
    }
  }
}

child_template = {
          "mirror": False,
          "mcScale": 0.0,
          "offset": {
            "x": 0.0,
            "y": -0.0,
            "z": -0.0
          },
          "color": "0",
          "hidden": False,
          "texture": True,
          "nameColor": 0,
          "rotation": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
          },
          "show": True,
          "scale": {
            "x": 1.0,
            "y": 1.0,
            "z": 1.0
          },
          "textureSize": 1,
          "size": {
            "x": 1.0,
            "y": 1.0,
            "z": 1.0
          },
          "pos": {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0
          },
          "u": 0,
          "singleTex": False,
          "v": 0,
          "extrude": False,
          "recolor": False,
          "name": "Head Origin",
          "locked": False,
          "glow": False
        }

def to_vec3(v):
    return { 'x': v[0], 'y': v[1], 'z': v[2] }

def zy(v):
    return [v[0], -v[2], v[1]]

def inv_zy(v):
    return [v[0], v[2], -v[1]]

def vec3_add(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]

def vec3_sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

def add_child(child_obj, data, depth=0):
    child_data = child_template.copy()

    print('{} {}'.format(' '*depth, child_obj.name))

    child_data['name'] = child_obj.name
    child_data['pos'] = to_vec3(zy(child_obj.location))

    size = [max(corner[i] for corner in child_obj.bound_box) - min(corner[i] for corner in child_obj.bound_box) for i in range(3)]
    size[2] = -size[2]
    child_data['size'] = to_vec3(zy(size))

    rotation = child_obj.rotation_euler
    rotation = [math.degrees(i) for i in rotation]
    child_data['rotation'] = to_vec3(zy(rotation))

    offset = child_obj.data.vertices[1].co
    child_data['offset'] = to_vec3(zy(offset))

    child_data['show'] = not child_obj.hide_get()

    # faceUV
    order = [
        'west',
        'south',
        'east',
        'north',
        'down',
        'up',
    ]

    mesh = child_obj.data
    uv_layer = mesh.uv_layers.active.data
    rot = 0
    child_data['faceUV'] = {}
    for i, face in enumerate(child_obj.data.polygons):
        k = face.loop_start

        uvs = uv_layer[k + (2 + rot) % 4].uv
        uve = uv_layer[k + (0 + rot) % 4].uv
        child_data['faceUV'][order[i]] = {}

        child_data['faceUV'][order[i]]['sx'] = int(uvs[0] * data['skinSize']['x'])
        child_data['faceUV'][order[i]]['sy'] = int((1 - uvs[1]) * data['skinSize']['y'])
        child_data['faceUV'][order[i]]['ex'] = int(uve[0] * data['skinSize']['x'])
        child_data['faceUV'][order[i]]['ey'] = int((1 - uve[1]) * data['skinSize']['y'])
        child_data['faceUV'][order[i]]['rot'] = str(0)
        child_data['faceUV'][order[i]]['autoUV'] = False

    # children
    for child in child_obj.children:
        if 'children' not in child_data:
            child_data['children'] = []

        child_child_data = add_child(child, data, depth+1)
        if child_child_data is not None:
            child_data['children'].append(child_child_data)

    return child_data


def load(context,
         filepath,
         import_uvs = True,               # import face uvs
         import_textures = True,          # import textures into materials
         recenter_to_origin = True,       # recenter model to origin, overrides translate origin
         **kwargs):
    """Main export function"""

    cpmproject_file = tempfile.NamedTemporaryFile(suffix='.cpmproject', delete=False)
    cpmproject_file.close()

    try:

        with zipfile.ZipFile(cpmproject_file.name, "w") as zip_file:

            # texture
            skin = bpy.data.images.get('skin.png')

            data = data_template.copy()
            data['skinSize'] = {'x': skin.size[0], 'y': skin.size[1] }

            if skin is not None:
                skin_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                skin_file.close()
                skin.save_render(skin_file.name, scene=None)
                zip_file.write(skin_file.name, 'skin.png')

            for element in data['elements']:
                element_id = element['id']

                # go through the core parts
                root_object = bpy.data.objects.get(element_id)
                if root_object is None:
                    raise Exception('Missing core object \'{}\''.format(element_id))

                if element_id in alex_model:
                    model_pos = vec3_add(inv_zy(alex_model[element_id]['pos']), [0, 0, 24])
                    print(model_pos)
                    print(root_object.location)
                    pos = vec3_sub(root_object.location, model_pos)
                    print(pos)
                    element['pos'] = to_vec3(zy(pos))

                # if object is hidden disable
                if root_object.hide_get():
                    element['show'] = False

                for child in root_object.children:
                    if 'children' not in element:
                        element['children'] = []

                    child_data = add_child(child, data)
                    if child_data is not None:
                        element['children'].append(child_data)

            # write data
            with zip_file.open('config.json', 'w') as config_json:
                config_json.write(json.dumps(data).encode('utf-8'))

        # success, copy temp file to actual file
        shutil.move(cpmproject_file.name, filepath)

    finally:
        pass

    return {'FINISHED'}
