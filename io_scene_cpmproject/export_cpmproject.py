import zipfile
import json
import bpy
import tempfile
import shutil

data = {
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

            for element in data['elements']:
                element_id = element['id']

                # go through the core parts
                root_object = bpy.data.objects.get(element_id)
                if root_object is None:
                    raise Exception('Missing core object {}'.format(element_id))

            # write data
            with zip_file.open('config.json', 'w') as config_json:
                config_json.write(json.dumps(data).encode('utf-8'))

            # texture
            skin = bpy.data.images.get('skin.png')

            if skin is not None:
                skin_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                skin_file.close()
                skin.save_render(skin_file.name, scene=None)
                zip_file.write(skin_file.name, 'skin.png')

        # success, copy temp file to actual file
        shutil.move(cpmproject_file.name, filepath)

    finally:
        pass

    return {'FINISHED'}
