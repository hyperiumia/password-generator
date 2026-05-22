"""Command-line interface using argparse and rich."""

import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

from src.config import (
    APP_NAME, APP_VERSION, APP_AUTHOR,
    DEFAULT_LENGTH, DEFAULT_COUNT, MAX_LENGTH,
)
from src.generator import PasswordGenerator
from src.analyzer import PasswordAnalyzer

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="password-generator",
        description=f"{APP_NAME} v{APP_VERSION} — Generate cryptographically secure passwords",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python main.py                          # 1 password, 16 chars\n"
               "  python main.py -n 5 -l 24              # 5 passwords, 24 chars\n"
               "  python main.py --pronounceable --copy   # Pronounceable + clipboard\n"
               "  python main.py --no-symbols -l 8        # PIN-style, no symbols\n",
    )
    parser.add_argument("-n", "--count", type=int, default=DEFAULT_COUNT, help=f"Number of passwords (default: {DEFAULT_COUNT})")
    parser.add_argument("-l", "--length", type=int, default=DEFAULT_LENGTH, help=f"Password length (default: {DEFAULT_LENGTH}, max: {MAX_LENGTH})")
    parser.add_argument("--no-upper", action="store_true", help="Exclude uppercase")
    parser.add_argument("--no-lower", action="store_true", help="Exclude lowercase")
    parser.add_argument("--no-digits", action="store_true", help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    parser.add_argument("--pronounceable", action="store_true", help="Pronounceable passwords")
    parser.add_argument("--copy", action="store_true", help="Copy first password to clipboard")
    return parser


def print_banner():
    banner = Text()
    banner.append(f"  {APP_NAME}", style="bold cyan")
    banner.append(f" v{APP_VERSION}", style="dim")
    banner.append(f"\n  {APP_AUTHOR}", style="dim cyan")
    console.print(Panel(banner, border_style="cyan", padding=(0, 2)))


def display_passwords(passwords: list[str], analyzer: PasswordAnalyzer):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Password", style="bold", min_width=20)
    table.add_column("Length", justify="center", width=8)
    table.add_column("Entropy (bits)", justify="center", width=14)
    table.add_column("Strength", min_width=16)

    for i, pwd in enumerate(passwords, 1):
        analysis = analyzer.analyze(pwd)
        strength_text = Text()
        strength_text.append(f"{analysis.strength_bar} ", style=analysis.strength_color)
        strength_text.append(analysis.strength_label, style=analysis.strength_color)
        table.add_row(str(i), analysis.password, str(analysis.length), f"{analysis.entropy:.1f}", strength_text)

    console.print()
    console.print(table)
    console.print()


def run(args: argparse.Namespace):
    print_banner()
    try:
        generator = PasswordGenerator(
            length=args.length,
            use_upper=not args.no_upper,
            use_lower=not args.no_lower,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            pronounceable=args.pronounceable,
        )
        passwords = generator.generate_multiple(args.count)
    except ValueError as e:
        console.print(f"[red bold]Error:[/red bold] {e}")
        sys.exit(1)

    analyzer = PasswordAnalyzer()
    display_passwords(passwords, analyzer)

    if args.copy:
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(passwords[0])
            display = passwords[0][:20] + "..." if len(passwords[0]) > 20 else passwords[0]
            console.print(f"  [green]✓[/green] Copied to clipboard: [bold]{display}[/bold]")
        else:
            console.print("  [yellow]⚠[/yellow] pyperclip not installed. Install with: pip install pyperclip")
