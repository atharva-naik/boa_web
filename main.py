# from boa_web.Widgets import LabelWidget
import boa_web.Widgets as bwx
from boa_web.Browser import BoaCage, Page

if __name__ == '__main__':
    import time
    
    frame = bwx.LabelWidget(text="")
    label1 = bwx.LabelWidget(frame, text="this is the first one")
    label1.pack(align=bwx.LEFT)
    def click_callback(): print("button was clicked")
    button = bwx.ButtonWidget(label1, text="click me!")
    button.pack(align=bwx.LEFT)
    button.bind("click", click_callback)
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
#     boa.setZoomFactor(scale=5)
#     boa.alert("wow wow")