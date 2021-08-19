# python wrappers for css APIs
import os, pathlib, requests
KNOWN_CSS_SOURCES = {
                     "quill": ["https://cdn.quilljs.com/1.3.6/quill.snow.css"],
                     "bootstrap": ["https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"],
                     "codemirror": ["https://codemirror.net/lib/codemirror.css", 
                     "https://codemirror.net/theme/abbott.css"],
                     }


class StyleBuilder:
    def __init__(self, sources=KNOWN_CSS_SOURCES, static="./static/", download=True, force_download=False):
        self.static = static
        self.css_sources = sources
        self.exists = {}
        self.file_map = {}
        self.includes = []
        self.download = download
        self.force_download = force_download
        for name, urls in self.css_sources.items():
            for url in urls: 
                print(url)
                self.add_stylesheet(url)

    def _fetch(self, url, filename):
        open(filename, "w").write(requests.get(url).text)

    def add_stylesheet(self, url):
        '''return value is 'True' if the file has been downloaded locally'''
        filename = pathlib.Path(url).name
        static_url = "{{ "+f"url_for('static', filename='{filename}')"+" }}"
        filename = os.path.join(self.static, filename)
        self.exists[url] = os.path.exists(filename)
        self.includes.append(f'''<link rel="stylesheet" href="{static_url}">''')
        if self.force_download: 
            self._fetch(url, filename)
            self.exists[url] = True
        if not self.exists[url]:
            if self.download: self._fetch(url, filename)
            else: self.includes.append(f'''<link rel="stylesheet" href="{url}">''')
        self.file_map[url] = filename
        
        return True if self.exists[url] else False
