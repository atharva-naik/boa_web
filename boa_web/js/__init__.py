# python wrappers for javascript APIs
# try: from pdf import pdf
# except ImportError: from .pdf import pdf
try: 
    from quill import QuillJSPlugin
    from require import RequireJSPlugin
except ImportError: 
    from .quill import QuillJSPlugin
    from .require import RequireJSPlugin

quill = QuillJSPlugin()
require = RequireJSPlugin()

