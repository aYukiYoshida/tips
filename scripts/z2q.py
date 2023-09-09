from argparse import ArgumentParser, Namespace
from libs import z2q

def main() -> None:
    parser = ArgumentParser(
        description="Convert article of Zenn to one of Qiita",
    )
    parser.add_argument(
        "article_id",
        type=str,
        metavar="id",
        help="ID of the article of Zenn to convert",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        type=int,
        default=2,
        metavar="NUM",
        choices=range(4),
        help="Specify log level as an integer number",
    )

    args: Namespace = parser.parse_args()
    z2q(**vars(args))


if __name__ == "__main__":
    main()
