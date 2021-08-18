try:
    from plugin import JSPlugin
except ImportError:
    from .plugin import JSPlugin

class RequireJSPlugin(JSPlugin):
    def __init__(self, **kwargs):
        super(RequireJSPlugin, self).__init__(name="quill",
                                              static="./static/",
                                              cdn_urls=["https://cdnjs.cloudflare.com/ajax/libs/require.js/1.0.8/require.js"],
                                              cdn_min_urls=["https://cdnjs.cloudflare.com/ajax/libs/require.js/1.0.8/require.min.js"], 
                                              **kwargs)