import pytest
from time import sleep


def main():
    res = pytest.main(["."])
    sleep(30)
    quit(int(res))


if __name__ == "__main__":
    main()
