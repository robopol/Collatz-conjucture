from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
import matplotlib.pyplot as plt

# designate form  .kv file
Builder.load_string("""
<P>:
    Label:
        text: "Please enter a integer number"
        size_hint: 0.6, 0.2
        pos_hint: {"x":0.2, "top":1}    

<CollatzLayout>
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height
        padding: 50
        spacing: 10        
        Label:
            id: label_1
            text: "Begin / Number"
            font_size: 20
        TextInput:
            id: textinput_1
            text: ""
            font_size: 20
            halign:"right"
            multiline: False            
        Label:
            id: label_2
            text: "End / Number"
            font_size: 20
        TextInput:
            id: textinput_2
            text: ""
            font_size: 20
            halign:"right"
            multiline: False
        Label:
            id: label_3
            text: ""
            font_size: 14            
        Button:
            id: button_1
            text: "START"
            font_size: 20
            on_press: root.calculate()
""")
# Set the app size
Window.size = (350, 400)

class P(FloatLayout):
    pass
# function show a popup window
def show_popup():
    show = P()
    popupWindow = Popup(title="Error", content=show, size_hint=(None,None),size=(250,150))
    popupWindow.open()

class CollatzLayout(Widget):    
    # get input first
    def get_input_first(self):
        for i in range(len(self.ids.textinput_1.text)):
            if self.ids.textinput_1.text[i] not in '0123456789':
                show_popup()
                return 1
            else:
                num_first = int(self.ids.textinput_1.text)  
                return num_first            
        
    # get input second
    def get_input_second(self):
        if self.ids.textinput_2.text == "":
            return 1
        else:
            for i in range(len(self.ids.textinput_2.text)):
                if self.ids.textinput_2.text[i] not in '0123456789':
                    show_popup()
                    return 1
                else:
                    num_second = int(self.ids.textinput_2.text)
                    return num_second

        # calculate collatz 
    def calculate(self):                
        num_first = self.get_input_first()                  
        num_second = self.get_input_second()
        if num_second == None or num_second <= num_first:
            # define constant
            x=num_first; x_max=num_first            
            field_num=[num_first]
            # calculate collatz loop
            while x != 1:
                if x % 2 == 0:
                    x = x // 2
                    field_num.append(x)
                else:
                    x = 3 * x + 1
                    field_num.append(x)
                    if x > x_max: x_max = x
            
            # plot a sequence graph            
            plt.title(f'Collatz sequence for x={num_first}, max = {x_max}')
            plt.grid(True)
            plt.xlabel("number in sequence")
            plt.ylabel("value Collatz")
            plt.plot(field_num) 
            plt.show()
            self.ids.label_3.text = f'Max value for Collatz sequence:\n for n={num_first}\n is {x_max}'
            
        if num_second != None and num_second > num_first:
            # define constant
            x=num_first
            x_field=num_first
            y=num_second-num_first
            x_max=num_first
            field_x=[];field_y=[]            
            # calculate collatz loop
            max_x=num_first
            while x_field<=num_first+y:
                x=x_field; x_max=x_field
                while x != 1:
                    if x % 2 == 0:
                        x = x // 2                              
                    else:
                        x = 3 * x + 1
                        if x > x_max: x_max = x
                field_x.append(x_field)
                field_y.append(x_max)
                if x_max > max_x: max_x = x_max
                x_field +=1
            
            # plot a sequence graph
            plt.title(f'Maximum value for Collatz sequence: for x={num_first} ... {num_second} is {max_x}')
            plt.grid(True)           
            plt.xlabel("x in sequence")
            plt.ylabel("Max value Collatz")
            plt.plot(field_x,field_y) 
            plt.show()
            self.ids.label_3.text = f'Max value for Collatz sequence:\n for n={num_first} ... {num_second}\n is {max_x}'
        return

class CollatzConjucture(App):
    def build(self):
        return CollatzLayout()

if __name__=="__main__":
    CollatzConjucture().run()


