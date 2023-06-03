from UGChordsSite import UGChordsSite
from TAB4UChordsSite import TAB4UChordsSite
import multiprocessing


def populate_site_list(url, site_name, max_line_len, chords_site_list):
    if site_name == 'UG':
        abc = UGChordsSite(url, max_line_len)
        print(abc)
        print("about to append...")
        chords_site_list.append(abc._language)
    if site_name == 'TAB4U':
        chords_site_list.append(TAB4UChordsSite(url, max_line_len))


class ChordsSiteList:

    _file_name = None
    _site_name = None
    _urls_file_path = None
    _chords_site_list = None
    _max_line_len = None

    def __init__(self, urls_file_path, max_line_len, site_name):
        self._file_name = urls_file_path.split('/')[-1].split('.')[0]
        self._site_name = site_name
        self._urls_file_path = urls_file_path
        self._max_line_len = max_line_len
        self.parse_urls()
        self.sort()

    def parse_urls(self):

        def load_pages_in_parallel():
            chunk_size = 1
            url_list_chunks = [urls[i:i+chunk_size] for i in range(0, len(urls), chunk_size)]
            with multiprocessing.Manager() as manager:
                shared_list = manager.list()
                for url_batch in url_list_chunks:
                    parallel_execution = multiprocessing.Pool()
                    args = [(url, self._site_name, self._max_line_len, shared_list) for url in url_batch]
                    parallel_execution.starmap(populate_site_list, args)
                    parallel_execution.close()
                    parallel_execution.join()
                    print(shared_list)

        # Read the list of URLs from an external file
        with open(self._urls_file_path) as f:
            urls = f.readlines()
            # Remove whitespace characters like `\n` at the end of each line
            urls = [url.strip() for url in urls]

        # Iterate over the list of URLs
        self._chords_site_list = []
        load_pages_in_parallel()

    def sort(self):
        self._chords_site_list.sort(key=lambda site: (site.get_title()))

    def get_list(self):
        return self._chords_site_list

    def get_language(self):
        if self._site_name == 'UG':
            return 'EN'
        if self._site_name == 'TAB4U':
            return 'HE'

    def get_setlist(self):
        setlist = []
        for chords_site in self._chords_site_list:
            setlist.append(chords_site.get_title())
        return setlist

    def get_file_name(self):
        return self._file_name


def test():
    urls_file_path = 'URLs/UG-test.txt'
    chords_site_list = ChordsSiteList(urls_file_path, 150, 'UG')
    print (chords_site_list._chords_site_list[0]._song_name)
    chords_site_list.sort()
    print (chords_site_list._chords_site_list[0]._song_name)


if __name__ == '__main__':
    test()
