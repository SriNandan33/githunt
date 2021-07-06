""" Formats repositories in console """

# Standard library imports
import textwrap
from sys import stderr

# Third party imports
from colorama import init, Fore, Style
from tabulate import tabulate



def eprint(string):
    """ Prints a string to stderr. """
    print(string, file=stderr)

def make_hyperlink(text, target):
    """ Makes hyperlink out of text and target and retuns it
        https://stackoverflow.com/questions/44078888/clickable-html-links-in-python-3-6-shell
    """
    return f"\u001b]8;;{target}\u001b\\{text}\u001b]8;;\u001b\\"


def colored_output(repos, output):
    """ Displays repositories using colorama """

    init()  # initialize coloroma
    seperator = "+==================================================================+"
    print(Fore.WHITE, Style.BRIGHT, seperator, end="\n\n")
    for repo in repos:
        print(
            Fore.LIGHTRED_EX,
            Style.BRIGHT,
            f"{make_hyperlink(repo['name'], repo['html_url'])}",
        )
        print(
            Fore.LIGHTYELLOW_EX,
            Style.NORMAL,
            "\n  ".join(textwrap.wrap(f"{repo['description']}", len(seperator))),
            end="\n\n",
        )
        print(Fore.LIGHTCYAN_EX, Style.BRIGHT, repo['language'], end="\t")
        print(
            Fore.LIGHTCYAN_EX,
            Style.BRIGHT,
            f"{repo['stargazers_count']} Stars",
            end="\t",
        )
        print(Fore.LIGHTCYAN_EX, Style.BRIGHT, f"{repo['forks_count']} Forks", end="\t")
        print(
            Fore.LIGHTCYAN_EX,
            Style.BRIGHT,
            f"{repo['watchers_count']} Watchers",
            end="\n\n",
        )
        print(Fore.WHITE, Style.BRIGHT, seperator, end="\n\n", file=output)


def tabular_output(repos, output):
    """ Displays repositories as tables using tabulate """
    table_headers = ["URL", "Language", "Stars", "Forks", "Watches"]
    repositories = [
        [
            repo["html_url"],
            repo["language"],
            repo["stargazers_count"],
            repo["forks_count"],
            repo["watchers_count"],
        ]
        for repo in repos
    ]
    print(tabulate(repositories, headers=table_headers, tablefmt="fancy_grid"), file=output)


def beautify(repos, fmt, output):
    """ Beautfies the output based on the display format given """
    if fmt == "colored":
        colored_output(repos, output)
    elif fmt == "table":
        tabular_output(repos)
    else:
        eprint("Can't output anything. Invalid display format!")
