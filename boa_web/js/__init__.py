# python wrappers for javascript APIs
# try: from pdf import pdf
# except ImportError: from .pdf import pdf
DOWNLOAD_JS = True

try: 
    from quill import QuillJSPlugin
    from require import RequireJSPlugin
except ImportError: 
    from .quill import QuillJSPlugin
    from .require import RequireJSPlugin

quill = QuillJSPlugin(download=DOWNLOAD_JS)
require = RequireJSPlugin(download=DOWNLOAD_JS)
CustomPlugins = {"quill": quill, 
                 "require": require}