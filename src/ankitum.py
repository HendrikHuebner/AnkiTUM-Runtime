from typing import Any

import click
import yaml

from src.generator import generate_flashcards


@click.command()
@click.argument("input_file", type=click.File(mode="r"))
@click.option("--output", "-o", type=click.Path(), help="Output flashcards file")
@click.option("--debug", is_flag=True, help="Enable debug mode")
def generate(input_file, output, debug):
    """Generate flashcards from a Yaml file."""

    root = yaml.load(input_file, Loader=yaml.FullLoader)

    if "title" not in root or not isinstance(root["title"], str):
        click.echo("Parsing error: Missing deck title attribute")
        exit(1)

    if "cards" not in root or not isinstance(root["cards"], list):
        click.echo("Parsing error: Missing cards attribute")
        exit(1)

    title: str = root["title"]
    cards: list[Any] = root["cards"]
    authors: list[str] = []

    if "authors" in root:
        if isinstance(root["authors"], str):
            authors.append(root["authors"])

        elif isinstance(root["authors"], list):
            for author in root["authors"]:
                if isinstance(author, str):
                    authors.append(author)

    if debug:
        click.echo(f"Parsed deck with title=\"{title}\" authors=\"{authors}\" and a list of {len(cards)} cards.")

    generate_flashcards(title, authors, cards)


if __name__ == "__main__":
    generate()