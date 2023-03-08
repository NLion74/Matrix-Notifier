import pytest
import time


def main():
    res = pytest.main(["."])
    quit(int(res))


if __name__ == "__main__":
    main()
