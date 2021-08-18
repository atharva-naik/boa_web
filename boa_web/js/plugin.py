import os, requests, pathlib


class JSPlugin:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.name = "plugin" # the name of the javasrcipt plugin
        self.static = self.kwargs.get("static", "./static/") # path of static folder
        self.cdn_urls = kwargs.get("cdn_urls", ["https://www.cdn.com/<plugin>.js"]) # cdn urls to formatted js
        self.cdn_min_urls = kwargs.get("cdn_min_urls", ["https://www.cdn.com/<plugin>.min.js"]) # cdn urls to minified js
        self.file_map = {}
        for url in self.cdn_urls+self.cdn_min_urls: 
            self.file_map[url] = os.path.join(self.static, pathlib.Path(url).name)
        self.download = self.kwargs.get("download", True) # download to static (cdn is used otherwise)
        self.force_download = self.kwargs.get("force_download", False) # force download from cdn link every time. 
        self.use_cdn = not(self.download) # use from cdn
        self._codes = [] # save codes if file is being downloaded
        self._fetch() # fetch js files if needed
        # self.includes = self._includes()

    def _fetch(self):
        if self.download:
            for i,url in enumerate(self.cdn_urls):
                path = self.file_map[url]
                if self.force_download or not os.path.exists(path):
                    self._codes.append(requests.get(url).text)
                    open(path, "w").write(self._codes[-1])
    # def _includes(self):
    #     includes = []
    #     for url in self.cdn_min_urls:
    #         if self.use_cdn: 
    #             includes.append(f'''<script src="{url}"></script>''')
    #         else:
    #             static_url = "{{ "+f"url_for('static', '{self.name}')"+" }}"
    #             includes.append(f'''<script src="{static_url}"></script>\n''')

    #     return includes
    def __str__(self):
        includes = ""
        for url in self.cdn_min_urls:
            if self.use_cdn: 
                includes += f'''<script src="{self.cdn_min_url}"></script>\n'''    
            else:
                static_url = "{{ "+f"url_for('static', '{self.name}')"+" }}"
                includes += f'''<script src="{static_url}"></script>\n'''

        return includes