parse_warnings.py


import argparse
import csv
import re
from pathlib import Path

WARNING = re.compile(r"(.+?):[ \t]*([0-9]+):[ \t]*warning:[ \t]*(.*)")

def main():
    parser = argparse.ArgumentParser(description="Convert Doxygen warnings to CSV.")
    parser.add_argument("warnings_log", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("warnings.csv"))
    args = parser.parse_args()

    if args.warnings_log.resolve() == args.output.resolve():
        parser.error("The output must be a different file from the warnings log.")

    with args.warnings_log.open(encoding="utf-8", errors="replace") as source:
        with args.output.open("w", encoding="utf-8", newline="") as output:
            writer = csv.writer(output)
            writer.writerow(("Line", "File", "Message"))

            for line in source:
                match = WARNING.fullmatch(line.rstrip("\r\n"))
                if match:
                    filename, line_number, message = match.groups()
                    writer.writerow((line_number, filename, message))


if __name__ == "__main__":
    main()
