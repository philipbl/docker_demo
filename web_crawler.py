from datetime import datetime
import time
from collections import Counter
from zoneinfo import ZoneInfo


from bs4 import BeautifulSoup
import requests

root_url = "https://byu-cpe.github.io"
urls_to_visit = ["/ComputingBootCamp/"]
visited_urls = []
word_count = Counter()

now = datetime.now(tz=ZoneInfo("US/Mountain"))
print(f"Started at {now}")

while len(urls_to_visit) > 0:
    url = urls_to_visit.pop()
    full_url = root_url + url
    # print(f"Visiting {full_url}")

    response = requests.get(full_url)
    visited_urls.append(url)

    try:
        html = response.content.decode()
    except UnicodeDecodeError:
        continue

    soup = BeautifulSoup(html, "html.parser")

    for string in soup.stripped_strings:
        word_count.update(string.split(" "))

    for link in soup.find_all("a"):
        href = link.get("href")

        if href is None:
            continue

        if (
            len(href) > 0
            and href[0] == "/"
            and href not in visited_urls
            and href not in urls_to_visit
        ):
            urls_to_visit.append(href)

    # time.sleep(1)
    print(word_count.most_common(5))

print("#" * 80)
print(f"Links visited: {len(visited_urls)}")
for url in sorted(visited_urls):
    print(url)
