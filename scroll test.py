from functools import partial

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.stacklayout import StackLayout


class ScrollApp(App):
    def build(self):
        popup = Popup(title='Draggable Scrollbar', size_hint=(0.8, 1), auto_dismiss=False)

        # this layout is the child widget for the main popup
        layout1 = StackLayout(orientation='lr-bt')

        # this button is a child of layout1
        closebutton = Button(text='close', size_hint=(0.9, 0.05))
        closebutton.bind(on_press=popup.dismiss)

        # another child of layout1 and this is the scrollview which will have a custom draggable scrollbar
        scrlv = ScrollView(size_hint=(0.9, 0.95))

        # the last child of layout1 and this will act as the draggable scrollbar
        s = Slider(min=0, max=1, value=25, orientation='vertical', step=0.01, size_hint=(0.1, 0.95))

        scrlv.bind(scroll_y=partial(self.slider_change, s))

        # what this does is, whenever the slider is dragged, it scrolls the previously added scrollview by the same
        # amount the slider is dragged
        s.bind(value=partial(self.scroll_change, scrlv))

        layout2 = GridLayout(cols=4, size_hint_y=None)
        layout2.bind(minimum_height=layout2.setter('height'))
        for i in range(1, 301):
            btn = Button(text=str(i), size_hint_y=None, height=60, valign='middle', font_size=12)
            btn.text_size = (btn.size)
            layout2.add_widget(btn)
        scrlv.add_widget(layout2)
        layout1.add_widget(closebutton)
        layout1.add_widget(scrlv)
        layout1.add_widget(s)
        popup.content = layout1
        popup.open()

    def scroll_change(self, scrlv, instance, value):
        scrlv.scroll_y = value

    def slider_change(self, s, instance, value):
        if value >= 0:
            # this to avoid 'maximum recursion depth exceeded' error
            s.value = value


if __name__ == '__main__':
    ScrollApp().run()
