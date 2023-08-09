import os
import json

import argparse


def get_args():
    parser = argparse.ArgumentParser(description="This script takes the original metadata files given by the SparseLibriMix repo and fixes the mixture ids to the more meaningful version. It saves the new version with the same name as the given file and backs up the original file with a .backup extension.")

    parser.add_argument("--metadata_file", help="The path to the metadata file to be fixed")

    args = parser.parse_args()
    return args


def main():
    args = get_args()

    with open(args.metadata_file, "r") as f:
        total_metadata = json.load(f)

    for c_mixture in total_metadata:
        assert c_mixture["mixture_name"].startswith("mix_"), "The original metadata files have the mixture names in the format mix_xxxxxx."

        spk_keys = [elem for elem in c_mixture.keys() if elem.startswith("s")]
        spk_keys.sort()
        utt_id_list = [c_mixture[c_key][0]["utt_id"] for c_key in spk_keys]

        new_mix_id = "_".join(utt_id_list)
        c_mixture["mixture_name"] = new_mix_id

    os.rename(args.metadata_file, f"{args.metadata_file}.backup")
    with open(args.metadata_file, "w") as f:
        json.dump(total_metadata, f, indent=4)


if __name__ == "__main__":
    main()
