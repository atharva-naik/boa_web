class JSPlugin:
    import os
    def __init__(self, **kwargs):
        import os
        self.name = "<plugin>.js"
        self.cdn_url = "https://www.cdn.com/<plugin>.js"
        self.cdn_min_url = "https://www.cdn.com/<plugin>.min.js"
        self.kwargs = kwargs
        self.static = self.kwargs.get("static", "./static/")
        self.path = os.path.join(self.static, self.name)
        self.download = self.kwargs.get("download", True)
        self.force_reload = self.kwargs.get("force_reload", False)

    def _fetch(self):
        pass