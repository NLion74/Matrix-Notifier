import coverage


def main():
    cov = coverage.Coverage()
    cov.combine("../docker/data")


if __name__ == "__main__":
    main()
