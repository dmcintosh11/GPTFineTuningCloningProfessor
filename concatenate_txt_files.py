import os
import glob

def concatenate_files(input_files, output_file):
    with open(output_file, "w") as outfile:
        for input_file in input_files:
            with open(input_file, "r") as infile:
                content = infile.read()
                outfile.write(content)
                outfile.write("\n")  # Add a newline between concatenated files

if __name__ == "__main__":
    input_files = glob.glob("*_transcript.txt")
    output_file = "concatenated_videos.txt"

    if input_files:
        concatenate_files(input_files, output_file)
        print(f"Concatenated {len(input_files)} files into '{output_file}'.")
    else:
        print("No 'video_*.txt' files found in the current directory.")
