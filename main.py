#!/usr/bin/env python3
"""Password Generator Pro — Entry Point. Built by Patricio Tirado (Hyperium IA)."""

from src.cli import build_parser, run


def main():
    parser = build_parser()
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
