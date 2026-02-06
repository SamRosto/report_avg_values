import asyncio
import csv
import tabulate
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Mean GDP by country')
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--report", required=True)

    return parser.parse_args()


async def main():
    parsed_args = parse_args()
    print(parsed_args.files)
    print(parsed_args.report)


if __name__ == "__main__":
    asyncio.run(main())