# from boa_web.Widgets import LabelWidget
import boa_web.Widgets as bwx
from boa_web.Browser import BoaCage, Page


class CustomButton(bwx.ButtonWidget):
     def __init__(self, parent, text="", **attrs):
          super(CustomButton, self).__init__(parent=parent, text=text, **attrs)
          self.ctr = 0

     def onclick(self):
          self.ctr += 1
          if self.ctr%2 == 0: self.setStyle(background_color='red')
          else: self.setStyle(background_color='green')


class CustomImage(bwx.BImage):
     def __init__(self, source, parent=None, **kwargs):
          super(CustomImage, self).__init__(source=source, parent=parent, **kwargs)
          self.bind('mouseenter', self.onmouseenter)
          self.bind('mouseleave', self.onmouseleave)

     def onmouseenter(self):
          print("cursor entered the image")

     def onmouseleave(self):
          print("cursor exited the image")

if __name__ == '__main__':
     import time
    
     frame = bwx.LabelWidget(text="")
     label1 = bwx.LabelWidget(frame, text="this is the first one")
     label1.pack(align=bwx.LEFT)
     def click_callback(): 
          print("button was clicked")
     button = CustomButton(label1, text="click me!")
     button.pack(align=bwx.LEFT)
     button.bind("click", button.onclick)
     img = CustomImage(source="logo.png", 
                       parent=frame, 
                       alt="boa image", 
                       height="100px", 
                       width="100px", 
                       title="this is an image")
     img.pack(align=bwx.CENTER)
#     label_inside_button = bwx.LabelWidget(button, text="innerHTML inside button div")
#     label_inside_button.pack()
     label2 = bwx.LabelWidget(frame, text="this is the second one")
     label2.pack(align=bwx.RIGHT)
     label3 = bwx.LabelWidget(frame, text="this is the third one")
     label3.pack(align=bwx.CENTER)
     page = Page(root=frame, 
                 title="My first app", 
                 footer="This is a footer", 
                 header="This is a header")
     page.build()
     page.save("templates/index.html")
     boa = BoaCage(__name__, 
                   port=5000, 
                   scale=2,
                   rotation=0,
                   title="boa: Hello World")
     boa.run()
     page.attach(boa)
     # boa.setZoomFactor(scale=5)
     # boa.alert("wow wow")