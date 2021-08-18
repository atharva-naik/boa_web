# from boa_web.Widgets import LabelWidget
import boa_web.js as js
import boa_web.css as css
import boa_web.Widgets as bwx
import boa_web.Browser as boa
import boa_web.managerAPI.Stats as stats


class CustomButton(bwx.ButtonWidget):
     def __init__(self, parent=None, text="", **attrs):
          super(CustomButton, self).__init__(parent=parent, text=text, **attrs)
          self.ctr = 0

     def onclick(self):
          self.ctr += 1
          if self.ctr%2 == 0: self.setStyle(background_color='red')
          else: self.setStyle(background_color='green')
class CustomProgressbar(bwx.ProgressbarWidget):
     def __init__(self, start=0, total=100, parent=None, **attrs):
          super(CustomProgressbar, self).__init__(start=start, total=total, parent=parent, **attrs)

     def tick(self, step):
          import time, colors
          #print(time.time())
          print(colors.color(f"callback called at {time.time()}", fg="yellow"))
          self.update(step)

class CustomImage(bwx.BImage):
     def __init__(self, source, parent=None, **kwargs):
          super(CustomImage, self).__init__(source=source, parent=parent, **kwargs)
          self.bind('mouseenter', self.onmouseenter)
          self.bind('mouseleave', self.onmouseleave)

     def onmouseenter(self):
          self.setAttr("src", "./static/google.png")
          print("cursor entered the image")

     def onmouseleave(self):
          self.setAttr("src", "./static/github.png")
          print("cursor exited the image")


if __name__ == '__main__':
     import time
    
     frame = bwx.LabelWidget(text="")
     label1 = bwx.LabelWidget(frame, text="this is the first one")
     label1.pack(align=bwx.LEFT)
     pbar = CustomProgressbar(20, 100, frame) # start with 20 on a progress bar that goes up to 100.
     pbar.pack()
     pbar.after(pbar.tick, T=1, step=2) # every 5 ms update progressbar by 2%

     button = CustomButton(label1, text="click me!")
     button.pack(align=bwx.LEFT)
     button.bind("click", button.onclick)
     
     video = bwx.VideoWidget(source="./earth.webm", parent=frame, width="300px")
     video.pack(align=bwx.LEFT)
     img = CustomImage(source="./boa_web/icons/earth.gif", parent=frame, alt="boa image", height="100px", width="100px", title="this is an image")
     img.pack(align=bwx.CENTER)

     label2 = bwx.LabelWidget(frame, text="this is the second one")
     label2.pack(align=bwx.RIGHT)
     label3 = bwx.LabelWidget(frame, text="this is the third one")
     label3.pack(align=bwx.CENTER)
     page = boa.Page(root=frame, title="My first app", footer="This is a footer", header="This is a header")
     # page.require(js.require)
     # page.require(js.quill)
     page.add_stylesheet(url="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css")
     page.add_script(url="https://code.jquery.com/jquery-3.2.1.slim.min.js")
     page.build()
     page.save("templates/index.html")
     Boa = boa.BoaCage(__name__, port=5000, scale=1, rotation=0, title="boa: Hello World")
     Boa.run()
     page.attach(Boa)
     perf_tracker = stats.PerformanceTracker()
     perf_tracker.start()
     # boa.setZoomFactor(scale=5)
     # boa.alert("wow wow")
     # label_inside_button = bwx.LabelWidget(button, text="innerHTML inside button div")
     # label_inside_button.pack()