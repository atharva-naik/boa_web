# ButtonWidget: <button> tag
# LabelWidget: <p> tag
import bs4 
try: from _utils import *
except ImportError: from ._utils import *

Widget2Tag = {"Label":"p", 
              "Button":"button",
              "Video":"video",
              "Image":"img",
              "Bar":"progress"}
LEFT = "left"
CENTER = "center"
RIGHT = "right"
DEFAULT_TOOLBAR = [[{'header': [1, 2, 3, 4, 5, 6, False]}],
                   ['bold', 'italic', 'underline', 'strike', {'script': 'sub'}, {'script': 'super'}],
                   ['blockquote', 'code-block', {'indent': '-1'}, {'indent': '+1'}],
                   [{'list': 'ordered'}, {'list': 'bullet'}],
                   ['image', 'link'],
                   [{'color': []}, {'background': []}, {'font': []}, {'align': []}]]

class Widget:
    def __init__(self, parent=None, text="", requires=[], **attrs):
        self._secret = rand_str()
        self.innerText = "" # innerText attribute of Node/Widget
        self.innerHTML = "" # innerHtml attribute of Node/Widget (including html of child)
        self.type = ""
        self.text = text
        self.cage = None
        self.requires = requires # list of JS libraries required
        self.tag = Widget2Tag.get(self.type, "span")
        self.soup = bs4.BeautifulSoup(self.innerHTML, features="html.parser")
        for attr,value in attrs.items():
            setattr(self, attr, value) # each attrinute of tag is attribute of the object now.
        self.attrs = attrs # dictionary of attributes.
        self.parent = parent
        self.children = []
        self.tab_level = "\t"
        self.is_packed = False
        self.align = LEFT
        if parent is not None:
            self.parent.children.append(self) # add current widget as a child for the parent.
        self._bindings = []

    def after(self, callback, T=1, repeat=True, **args):
        '''
        this callback is bound on the Python side.
        if repeat == True: the callback is called every x secs
        else: the callback is called only once
        time is in seconds
        '''
        import time, threading
        time.sleep(T)
        callback(**args)
        if repeat:
            backgroundThread = threading.Thread(target=self._after, args=(callback, args, T,))
            backgroundThread.start()

    def _after(self, callback, args, T):
        import time
        while True:
            time.sleep(T)
            callback(**args)
        # self._after(callback, args, T)
    def encage(self, cage):
        ''' Link a reference to the BoaCage instance for the widget and all of it's children '''
        self.cage = cage
        for child in self.children: child.encage(cage)

    def setAttr(self, attr, value):
        jscode = f'''element = document.getElementById("{self._secret}");\n'''
        jscode += f'''element.setAttribute("{attr.replace('-','_')}", "{value}");\n'''
        if self.cage: self.cage.execJS(jscode)        

    def setStyle(self, **attrs):
        jscode = f'''element = document.getElementById("{self._secret}");\n'''
        style_str = ""
        for attr, value in attrs.items():
            style_str += f"{attr.replace('_','-')}: {value};"
        jscode += f'''element.setAttribute("style", "{style_str}");\n'''
        # print(jscode)
        if self.cage: self.cage.execJS(jscode)

    def _compile(self, **attrs):
        attr_str = " ".join([f"{attr}={value}" for attr,value in self.attrs.items()]) 
        return f'''
<{self.tag} {attr_str}>
    {self.text}
    {self.innerHTML}
</{self.tag}>
'''

    def __str__(self):
        '''get the html of current widget including all children'''
        children_html = []
        for child in self.children:
            if child.is_packed:
                # child.tab_level += "\t" 
                children_html.append(f'''                
<div style="text-align: {child.align}">
    {str(child)}
</div>
''')
        self.innerHTML = "\n".join(children_html)
        self.soup = bs4.BeautifulSoup(self.innerHTML, features="html.parser")
        self.innerHTML = str(self.soup)
        self.innerText = self.soup.text
        attrs = self.attrs
        attrs["id"] = self._secret

        return self._compile(**attrs)

    def pack(self, **kwargs):
        self.align = kwargs.get("align", LEFT)
        self.is_packed = True

    def pack_forget(self, **kwargs):
        self.is_packed = False

    def setHTML(self, html):
        self.innerHTML = html
        self.soup = bs4.BeautifulSoup(self.innerHTML, features="html.parser")
        # self.innerHTML = str(self.soup)
        self.innerText = self.soup.text

    def setText(self, text):
        '''Need to decide whether to set innerText or text'''
        self.innerHTML = text
        self.innerText = text
        self.soup = bs4.BeautifulSoup(self.innerHTML, features="html.parser")
        # self.innerHTML = str(self.soup)

    def bind(self, event, callback):
        # print(event, callback)
        callback_name = f"{event}_{self._secret}"
        # setattr(self, callback_name, callback)
        js_callback = "function () {"+f"window.{callback_name}();"+"}"
        binding = f'''document.getElementById("{self._secret}").addEventListener('{event}', {js_callback} )
console.log('{callback_name} bound to {event} event of id={self._secret}');'''
        self._bindings.append({"name" : callback_name,
                               "callback": callback,# getattr(self, callback_name),
                               "jscode" : binding})

    def _get_bindings(self):
        rec_bindings = []
        for child in self.children:
            rec_bindings += child._get_bindings() 
        rec_bindings += self._bindings
        
        return rec_bindings

    def _get_requires(self):
        requires = []
        for child in self.children:
            requires += child._get_requires() 
        requires += self.requires
        
        return requires


class BImage(Widget):
    '''
    Class to represent the image tag. 
    This widget can display both images and gifs.
    '''
    def __init__(self, source, parent=None, **attrs):
        '''source url of the image is needed'''
        self.cage = None
        self.type = "Image"
        self._secret = rand_str()
        self.source = self.loadStatic(source)
        self.tag = Widget2Tag.get(self.type, "span")
        for attr,value in attrs.items():
            setattr(self, attr, value) # each attrinute of tag is attribute of the object now.
        self.attrs = attrs # dictionary of attributes.
        self.parent = parent
        self.is_packed = False
        self.tab_level = "\t"
        self.align = LEFT
        if parent is not None: self.parent.children.append(self) # add current widget as a child for the parent.
        self._bindings = []

    def loadStatic(self, path):
        import os, shutil, pathlib
        filename = pathlib.Path(path).name
        os.makedirs("static", exist_ok=True)
        filepath = os.path.join("./static", filename)
        shutil.copyfile(path, filepath)
        
        return filepath # filename

    def encage(self, cage):
        '''Link a reference to the BoaCage instance for the widget'''
        self.cage = cage   

    def _compile(self, src, **attrs):
        attr_str = " ".join([f"{attr}='{value}'" for attr,value in self.attrs.items()]) 
        # return f'''\n<{self.tag} src='''+'''{{'''+f''' url_for('static', filename='{src}') '''+'''}}'''+f''' {attr_str}>\n'''
        return f'''<{self.tag} src="{self.source}" {attr_str}>'''

    def __str__(self):
        '''get the html of current widget including all children'''
        attrs = self.attrs
        attrs["id"] = self._secret
        # attrs["src"] = self.source
        return self._compile(src=self.source, **attrs)
        
    def bind(self, event, callback):
        callback_name = f"{event}_{self._secret}"
        js_callback = "function () {"+f"window.{callback_name}();"+"}"
        binding = f'''document.getElementById("{self._secret}").addEventListener('{event}', {js_callback} )
console.log('{callback_name} bound to {event} event of id={self._secret}');'''
        self._bindings.append({"name" : callback_name,
                               "callback": callback,
                               "jscode" : binding})

    def _get_bindings(self):
        return self._bindings


class BAudio(Widget):
    def __init__(self,):
        pass


class LabelWidget(Widget):
    def __init__(self, parent=None, **attrs):
        super(LabelWidget, self).__init__(parent, **attrs)
        self.type = "Label"
        self.tag = Widget2Tag.get(self.type, "span")


class ButtonWidget(Widget):
    def __init__(self, parent=None, **attrs):
        super(ButtonWidget, self).__init__(parent, **attrs)
        self.type = "Button"
        self.tag = Widget2Tag.get(self.type, "span")

    def _compile(self, **attrs):
        attr_str = " ".join([f"{attr}={value}" for attr,value in self.attrs.items()]) 
        return f'''
<{self.tag} {attr_str}>
    {self.text}
</{self.tag}>
{self.innerHTML}'''


class VideoWidget(Widget):
    def __init__(self, source, parent=None, controls=True, **attrs):
        super(VideoWidget, self).__init__(parent, **attrs)
        self.type = "Video"
        self.controls = controls
        self.source = self.loadStatic(source)
        self.fromat = "mp4"
        self.tag = Widget2Tag.get(self.type, "span")

    def _compile(self, **attrs):
        attr_str = " ".join([f"{attr}={value}" for attr,value in self.attrs.items()])
        controls = 'controls' if self.controls else '' 
        return f'''
<video id={self._secret} src="{self.source}" type="video/{self.format}" {attr_str} {controls}>
</video>
'''

    def loadStatic(self, path):
        import os, shutil, pathlib
        filename = pathlib.Path(path).name
        self.format = path.split(".")[-1]
        os.makedirs("static", exist_ok=True)
        filepath = os.path.join("./static", filename)
        shutil.copyfile(path, filepath)
        
        return filepath

    def __str__(self):
        # self.soup = bs4.BeautifulSoup(self.innerHTML, features="html.parser")
        # self.innerHTML = str(self.soup)
        # self.innerText = self.soup.text
        attrs = self.attrs
        # attrs["id"] = self._secret
        return self._compile(**attrs)


class ProgressbarWidget(Widget):
    def __init__(self, start=0, total=100, parent=None, **attrs):
        super(ProgressbarWidget, self).__init__(parent, **attrs)
        self.type = "Bar"
        self.total = total
        self.tag = Widget2Tag.get(self.type, "span")
        self.current_progress = start

    def update(self, step=1):
        self.current_progress += step 
        self.setAttr(attr="value", value=self.current_progress)

    def _compile(self, **attrs):
        attr_str = " ".join([f"{attr}={value}" for attr,value in self.attrs.items()]) 
        return f'''
<progress id={self._secret} value="{self.current_progress}" max="{self.total}" {attrs}></progress>'''

    def __str__(self):
        attrs = self.attrs
        return self._compile(**attrs)


class RichTextWidget(Widget):
    def __init__(self, parent=None, static=False, **attrs):
        super(RichTextWidget, self).__init__(parent, 
                                             requires=['quill'],
                                             **attrs)
        self.type = "Bar"
        self.toolbar = attrs.get("toolbar", DEFAULT_TOOLBAR)
        self.placeholder = attrs.get("placeholder", "Your text here.")
        self.tag = Widget2Tag.get(self.type, "span")
        self.static = static # rely on the built page to include all necessary js
        self._secret = f"editor_{self._secret}"

    def _compile(self, **attrs):
        if self.static:        
            include = '''<script src="{{ url_for('static', filename='quill.js')}}"></script>''' 
        else: 
            include = '<script src="https://cdn.quilljs.com/1.3.6/quill.js"></script>'
        return f'''
<link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
<div id="{self._secret}"></div>
        {include}
        <script>
            var quill = new Quill('#{self._secret}', '''+"""{
                placeholder: '"""+self.placeholder+"""',
                modules: {
                    toolbar:"""+str(self.toolbar).replace('False','false')+'''
                },
                theme: 'snow'
            });
</script> 
'''


if __name__ == "__main__":
    LabelWidget(text="This is a label")
    print(str(LabelWidget))