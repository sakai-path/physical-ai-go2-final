#!/usr/bin/env python3
"""Check the four published artifacts used by the final Genesis evaluation.

Only run this against trusted files: torch.load/pickle.load may execute code.
"""
import argparse
import hashlib
import pickle
from pathlib import Path

import torch

FILES = {
    "locomotion": "phase112_final.pt",
    "cfg": "planned_cfgs.pkl",
    "pursuit": "upper_pursuit_12d_phase50.pt",
    "evasion": "upper_evasion_12d_phase50.pt",
}


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "models_dir", nargs="?", type=Path, default=Path("models"),
        help="Directory with four published model/config files (default: models)"
    )
    args = parser.parse_args()
    for role, filename in FILES.items():
        path = args.models_dir / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        print(f"{role}: {filename} bytes={path.stat().st_size} sha256={sha256(path)}")
        if role == "cfg":
            with path.open("rb") as stream:
                obj = pickle.load(stream)
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
    print("PASS: artifact format and structural checks (not a physics simulation)")


if __name__ == "__main__":
    main()
