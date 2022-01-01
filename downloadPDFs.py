from requests_html import HTMLSession
import wget
import os.path

session = HTMLSession()

url = f'https://www.mutopiaproject.org/ftp/'
fileType = "let.pdf"
r = session.get(url)
toPrint = []

# get all artists on the main page except the parent directory link
artists = r.html.xpath("//td[not(contains(a, 'Parent Directory'))]/a")
artists = [url + a.attrs["href"] for a in artists]
print(artists)

while len(artists) != 0:

    artistsCopy = artists
    for artist in artistsCopy:

        # if not the file to download continue down the tree
        if fileType not in artist:

            # make sure only valid links are being processed, and they're not the file we are looking for
            if artist[len(artist) - 1] != '/':
                artists.remove(artist)
                continue

            # get full working path
            r = session.get(artist)

            # get all sub-links besides the parent directory available
            sublinks = r.html.xpath("//td[not(contains(a, 'Parent Directory'))]/a")

            # add the remaining head links to the artists to sort and remove the current artist (replaced by its lower links [now visited])
            artists.remove(artist)
            artists += [artist + link.attrs["href"] for link in sublinks]

        # This is the file we want, add it to the to print list
        else:
            toPrint.append(artist)
            artists.remove(artist)
    print(artists)

print("\n\n\nTo Print:")
print(toPrint)

for file in toPrint:
    try:
        wget.download(file, f'/Users/download/path/{os.path.basename(file)}')
    except:
        print("A problem occurred")
