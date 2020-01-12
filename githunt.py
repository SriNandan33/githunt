""" Browse most stared repositories by date on Github """

import click
import requests

API_URL = "https://api.github.com/search/repositories"


@click.command()
@click.option("--language", default="", help="language filter (eg: python)")
def search(language):
    """ Returns repositories based on the language
        repositories are sorted by stars
    """
    filters = {"sort": "stars", "order": "desc", "q": f"language:{language}"}
    repositories = requests.get(API_URL, params=filters).json()
    print(repositories)


if __name__ == "__main__":
    search()
