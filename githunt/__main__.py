""" githunt.__main__ """

# Standard library imports
from datetime import datetime, timedelta
from sys import stdout

# Third party imports
import click
import requests

# Internal application imports
from .utils import beautify

API_URL = "https://api.github.com/search/repositories"


@click.command()
@click.option("--language", "-l", default="", help="Language filter (e.g. Python)")
@click.option(
    "--date",
    "-d",
    default="",
    help="ISO-8601-formatted date (YYYY-MM-DD)",
)
@click.option(
    "--fmt",
    "-f",
    default="colored",
    help="Output format (table or colored)",
)
@click.option(
    "--output",
    "-o",
    default="",
    help="File to pipe output to."
)
def search(language, date, fmt, output):
    """ 
    Returns repositories based on the language. Repositories are sorted by stars
    """
    if output == "":
        output = stdout

    if not date:
        start_date = datetime.fromisoformat(
            datetime.utcnow().date().isoformat()
        )  # today's timestamp in YYYY-MM-DD:00:00:00 format
        end_date = datetime.fromisoformat(
            (datetime.utcnow() + timedelta(days=1)).date().isoformat()
        )  # next day's timestamp in YYYY-MM-DD:00:00:00 format
    else:
        start_date = datetime.fromisoformat(date)
        end_date = datetime.fromisoformat(
            (start_date + timedelta(days=1)).date().isoformat()
        )

    query = f"stars:>0+created:{start_date.isoformat()}..{end_date.isoformat()}"
    query += f"+language:{language}" if language else ""
    url = f"{API_URL}?q={query}&sort=stars&order=desc"
    repositories = requests.get(url).json()
    beautify(repositories["items"], fmt, output)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    search()
