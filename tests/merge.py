import coverage
import sys


def main():
    cov = coverage.Coverage()
    cov.combine(data_paths=sys.argv[1])


if __name__ == "__main__":
    main()
