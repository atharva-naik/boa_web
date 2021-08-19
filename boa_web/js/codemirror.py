try:
    from plugin import JSPlugin
except ImportError:
    from .plugin import JSPlugin

class CodeMirrorJSPlugin(JSPlugin):
    def __init__(self, **kwargs):
        super(CodeMirrorJSPlugin, self).__init__(name="codemirror",
                                            static="./static/",
                                            cdn_urls=["https://codemirror.net/lib/codemirror.js", "https://codemirror.net/mode/python/python.js"],
                                            cdn_min_urls=[], 
                                            **kwargs)