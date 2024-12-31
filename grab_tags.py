import copy
import csv
import re
from bs4 import BeautifulSoup
import requests
import nanoid

CONST_A_PATTERN = re.compile(
    r'<a href="\/manga\/tags\/[a-zA-Z0-9\s-]*" itemprop="url">([a-zA-Z0-9\s-]*)<\/a>'
)


url = "http://192.168.1.34:8191/v1"

cookies = {
    "darkmode": "on",
    "cf_clearance": "GDRYpGK26okEg.iLIy6R8Xov5rLZ5G4f8jcHz2XWFcU-1735540060-1.2.1.1-U7xn3dX6pZ9k_fc5e05dgnCWYTGHWdahE_jBlcGJF4tvgDWB9q_B3_KawVgjj3DVxPK6E396qkuy2Ha9i20m6ezjv2axvJ_Z4g2DrzLHf7BrqKXyNFJJH8KQc65VZ8WBJNaAsBcrMgtVGhFgnLHrll5sM4LDuRS2mch8fHLyL7KPPGN6uBWQRbV1g6hncuDpJAykmF26fWdD3zZ8bicP.cgC_HzxOmaFyB3074vydVu6D3rHlnUez_KFWaUtECtjXRMyB._Oy.loXAMwf7kjY96mh3X2PJISmkXuw3aoT4WiJMro0QL7FTIXmEVA.twrblJR96gXwJlFDLs8dGH4oQ",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    "Referer": "https://www.anime-planet.com/manga/tags?page=2",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    # 'Cookie': 'darkmode=on; cf_clearance=GDRYpGK26okEg.iLIy6R8Xov5rLZ5G4f8jcHz2XWFcU-1735540060-1.2.1.1-U7xn3dX6pZ9k_fc5e05dgnCWYTGHWdahE_jBlcGJF4tvgDWB9q_B3_KawVgjj3DVxPK6E396qkuy2Ha9i20m6ezjv2axvJ_Z4g2DrzLHf7BrqKXyNFJJH8KQc65VZ8WBJNaAsBcrMgtVGhFgnLHrll5sM4LDuRS2mch8fHLyL7KPPGN6uBWQRbV1g6hncuDpJAykmF26fWdD3zZ8bicP.cgC_HzxOmaFyB3074vydVu6D3rHlnUez_KFWaUtECtjXRMyB._Oy.loXAMwf7kjY96mh3X2PJISmkXuw3aoT4WiJMro0QL7FTIXmEVA.twrblJR96gXwJlFDLs8dGH4oQ',
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0, i",
}

data = {
    "cmd": "request.get",
    "url": "https://www.anime-planet.com/manga/tags?page=1",
    "maxTimeout": 60000,
}


def main():
    a_tags = [["Tag", "Description", "ID", "Type"]]
    html_content = None

    for page in range(1, 21):
        data["url"] = "https://www.anime-planet.com/manga/tags?page=" + str(page)
        response = requests.post(url, headers=headers, json=data)
        print(response.status_code)
        html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")
        tags_table = soup.find("table")
        if not tags_table:
            print("Failed to find table in HTML response!")
            return

        for row in tags_table.find_all("tr"):
            tag = row.find("td")
            a = tag.find("a").get_text(strip=True)
            p = tag.find("p")
            if p:
                p = p.text.replace("\xa0", " ").replace("\\u2019", "'")

            a_tags.append([a, p, nanoid.generate(), "theme"])

    with open("tags.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, quotechar="\"", quoting=csv.QUOTE_MINIMAL, escapechar="\\")
        writer.writerows(a_tags)


if __name__ == "__main__":
    main()
