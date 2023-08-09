import argparse
import os
import json

import numpy as np


def get_args():
    parser = argparse.ArgumentParser(description="Obtain the rttm from a given metadata file for SparseLibriMix dataset")

    parser.add_argument("--metadata_file", help="The metadata file that contains the metadata information")
    parser.add_argument("--output_file", help="The output file where to save the resulting rttm file")

    args = parser.parse_args()

    return args


def main():
    args = get_args()

    with open(args.metadata_file, "r") as f:
        total_metadata = json.load(f)

    total_rttm = []
    for c_mixture in total_metadata:
        spk_keys = [c_key for c_key in c_mixture if c_key.startswith("s")]
        spk_keys.sort()
        for c_key in spk_keys:
            c_subutts = c_mixture[c_key]
            for sub_utt in c_subutts:
                c_spk_id = sub_utt["spk_id"]
                c_start = str(sub_utt["start"])
                c_dur = str(np.round(sub_utt["stop"] - sub_utt["start"], 3))
                c_mix_id = c_mixture["mixture_name"]

                c_rttm_entry = ["SPEAKER", c_mix_id, "1", c_start, c_dur, "<NA>", "<NA>", c_spk_id, "<NA>"]
                c_rttm_entry = "\t".join(c_rttm_entry)
                total_rttm.append(c_rttm_entry)

    total_rttm = "\n".join(total_rttm) + "\n"

    parent_folder = os.path.dirname(args.output_file)
    os.makedirs(parent_folder, exist_ok=True)

    with open(args.output_file, "w") as f:
        f.write(total_rttm)
    print(f"Done. Resulting rttm is saved in {args.output_file}")


if __name__ == "__main__":
    main()
