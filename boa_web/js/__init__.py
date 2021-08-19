# python wrappers for javascript APIs
# try: from pdf import pdf
# except ImportError: from .pdf import pdf
DOWNLOAD_JS = True

try: 
    from quill import QuillJSPlugin
    from require import RequireJSPlugin
    from codemirror import CodeMirrorJSPlugin
except ImportError: 
    from .quill import QuillJSPlugin
    from .require import RequireJSPlugin
    from .codemirror import CodeMirrorJSPlugin

quill = QuillJSPlugin(download=DOWNLOAD_JS)
require = RequireJSPlugin(download=DOWNLOAD_JS)
codemirror = CodeMirrorJSPlugin(download=DOWNLOAD_JS)
Plugins = {"quill": quill, 
           "require": require,
           "codemirror": codemirror,}