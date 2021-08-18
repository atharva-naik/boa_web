try:
    from plugin import JSPlugin
except ImportError:
    from .plugin import JSPlugin

class QuillJSPlugin(JSPlugin):
    def __init__(self, **kwargs):
        super(QuillJSPlugin, self).__init__(name="quill",
                                            static="./static/",
                                            cdn_urls=["https://cdn.quilljs.com/1.3.6/quill.js"],
                                            cdn_min_urls=["https://cdn.quilljs.com/1.3.6/quill.min.js"], 
                                            **kwargs)

# class QuillJSPlugin:
#     def __init__(self):
#         self.name = "quill.js"
#         self.cdn_url = ""

#     def save(self, path):
#         import os
#         # if not os.path.exists(path): open(path, "w").write(bytes(self._code).decode("iso 8859-15"))

#     def __str__(self):
#         static_url = "{{ "+f"url_for('static', '{self.name}')"+" }}"
#         return f'''<script src="{static_url}"></script>'''

#     def __repr__(self):
#         return self.__str__()