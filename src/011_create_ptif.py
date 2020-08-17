import os
import argparse
import sys
import glob

'''
python 011_create_ptif.py /Users/nakamurasatoru/git/d_sat/sat_images/docs/files/original/kandomokurokuJPEG /Users/nakamurasatoru/git/d_sat/sat_images/docs/files/tile/kandomokurokuJPEG tmp/test.sh
'''

def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'input_dir',
        action='store',
        type=str,
        help='Ful path to input dir.')

    parser.add_argument(
        'output_dir',
        action='store',
        type=str,
        help='Ful path to output dir.')

    parser.add_argument(
        'output_sh_file',
        action='store',
        type=str,
        help='Ful path to output sh file.')

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    output_path = args.output_sh_file

    output_path_dir = os.path.dirname(output_path)
    os.makedirs(output_path_dir, exist_ok=True)

    files = glob.glob(input_dir+"/**/*.jpg", recursive=True)

    files = sorted(files)

    f = open(output_path, 'w')

    for file in files:

        org_file_path = file
        new_file_path = org_file_path.replace(input_dir, output_dir)
        new_file_path = os.path.dirname(new_file_path) + "/" + os.path.splitext(os.path.basename(new_file_path))[0]+ ".tif"

        new_output_dir = os.path.dirname(new_file_path)

        f.write("mkdir -p " + new_output_dir + "\n")
        f.write("if [ ! -e \""+ new_file_path + "\" ]; then\n")
        f.write(
            "   convert \"" + org_file_path + "\" -define tiff:tile-geometry=256x256 -compress jpeg 'ptif:" + new_file_path + "'\n")
        f.write("fi\n")

    f.close()
