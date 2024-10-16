import requests
from bs4 import BeautifulSoup
import re


def scrape_hacker_news():
    """
    :return: retrieved entries
    """
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")  # returns a soup object

    entries = []
    titles = soup.select(".titleline")
    subtexts = soup.select(".subtext")

    for i in range(min(30, len(titles))):  # limit to first 30 entries
        url = titles[i].find("a").get("href")
        title = titles[i].find("a").get_text()

        subtext = subtexts[i].get_text()
        points = re.findall(r"(\d+) point", subtext)
        comments = re.findall(
            r"(\d+)\s*comment", subtext
        )  # special character between number and comment

        # parse points and comments to numbers
        points = int(points[0]) if points else 0
        comments = int(comments[0]) if comments else 0

        entries.append(
            {
                "number": i + 1,
                "title": title,
                "points": points,
                "comments": comments,
                "url": url,
            }
        )

    return entries
