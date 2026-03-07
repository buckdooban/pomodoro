import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("start", help="start the timer")
    args = parser.parse_args()
    print(args.start)


if __name__ == "__main__":
    main()
