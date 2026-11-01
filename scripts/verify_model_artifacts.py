#!/usr/bin/env python3
"""Local validation for the four artifacts used in the final Genesis evaluation.
Run in a trusted environment: torch.load/pickle can execute arbitrary code.
"""
import argparse
import hashlib
import pickle
from pathlib import Path

import torch

FILES = {
    "locomotion": "training/locomotion/phase112_78e8a86701/phase112_final.pt",
    "cfg": "training/locomotion/phase112_78e8a86701/planned_cfgs.pkl",
    "pursuit": "training/upper12_genesis/phase50_42b70a6b/upper_pursuit_12d_phase50.pt",
    "evasion": "training/upper12_genesis/phase50_42b70a6b/upper_evasion_12d_phase50.pt",
}

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("drive_root", type=Path, help="PhysicalAI_Go2_Pursuit directory")
    args = parser.parse_args()
    for role, relative in FILES.items():
        path = args.drive_root / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        print(f"{role}: {path.name} bytes={path.stat().st_size} sha256={digest(path)}")
        if role == "cfg":
            with path.open("rb") as f:
                obj = pickle.load(f)
            assert isinstance(obj, (tuple, list)) and len(obj) == 5
            assert len(obj[0]["joint_names"]) == 12
            print("  locomotion config: 12 joints / 5 sections OK")
        else:
            obj = torch.load(path, map_location="cpu", weights_only=False)
            assert isinstance(obj, dict)
            if role in ("pursuit", "evasion"):
                assert "actor_critic" in obj
                assert obj.get("config", {}).get("input_dim") == 12
                print("  upper policy: actor_critic / input_dim=12 OK")
            else:
                print("  locomotion checkpoint: dict OK")
    print("PASS: local file format and structural checks")

if __name__ == "__main__":
    main()
