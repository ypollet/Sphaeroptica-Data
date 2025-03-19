import sys
import json
import math
from photogrammetry import reconstruction, converters, helpers
import numpy as np

if len(sys.argv) < 2:
    print("Need a path")
    exit(404)

path = sys.argv[1]

with open(path, "r") as f:
    calib_file = json.load(f)


if "version" not in calib_file or calib_file["version"] == "1.0.0":
    calib_file["version"] = "2.0.0"
    intrinsics: dict = calib_file["intrinsics"]
    if "camera matrix" in intrinsics:
        intrinsics["cameraMatrix"] = intrinsics.pop("camera matrix")
    if "distortion matrix" in intrinsics:
        intrinsics["distortionMatrix"] = intrinsics.pop("distortion matrix")

    print(intrinsics.keys())

    intrinsics["cameraMatrix"]["matrix"] = (
        np.array(intrinsics["cameraMatrix"]["matrix"]).reshape(-1).tolist()
    )
    intrinsics["cameraMatrix"]["shape"] = (
        {
            "row": intrinsics["cameraMatrix"]["shape"][0],
            "col": intrinsics["cameraMatrix"]["shape"][1],
        },
    )

    intrinsics["distortionMatrix"]["matrix"] = (
        np.array(intrinsics["distortionMatrix"]["matrix"]).reshape(-1).tolist()
    )
    intrinsics["distortionMatrix"]["shape"] = (
        {
            "row": intrinsics["distortionMatrix"]["shape"][0],
            "col": intrinsics["distortionMatrix"]["shape"],
        },
    )

    for image_name in calib_file["extrinsics"]:
        calib_file["extrinsics"][image_name]["matrix"] = {
            "shape": {"row": 4, "col": 4},
            "matrix": np.array(calib_file["extrinsics"][image_name]["matrix"])
            .reshape(-1)
            .tolist(),
        }

if calib_file["version"] == "2.0.0":
    calib_file["version"] = "2.0.1"
    for image_name in calib_file["extrinsics"]:
        print(calib_file["extrinsics"][image_name]["matrix"]["matrix"][0:12])
        calib_file["extrinsics"][image_name]["matrix"] = {
            "shape": {"row": 3, "col": 4},
            "data": calib_file["extrinsics"][image_name]["matrix"]["matrix"][0:12],
        }

done = False
while not done:
    ret = input("Save it to same file ? (yes/no/cancel) : ")
    match ret:
        case "yes":
            done = True
            break
        case "no":
            path = input("Path of where to save : ")
            path = path if len(path) > 0 else "calib.json"
            done = True
            break
        case "cancel":
            exit(0)
        case _:
            done = False

with open(path, "w") as f:
    json.dump(calib_file, f)
