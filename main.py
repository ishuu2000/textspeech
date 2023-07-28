# main.py
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import speech_recognition as sr
from googletrans import Translator

class MyApp(App):
    def build(self):
        layout = FloatLayout()

        # User Interface Elements
        self.listen_button = Button(text='Listen', font_size='20sp', 
                                    on_press=self.listen_hindi, size_hint=(None, None), size=(120, 48),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.9})  # Positioned near the top center
        self.hindi_output = TextInput(multiline=True, font_size='20sp', font_name='NotoSans-Regular.ttf', 
                                      hint_text='Hindi text will appear here...',
                                      size_hint=(0.8, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.65})  # Positioned at the center
        self.translate_button = Button(text='Translate', font_size='20sp', 
                                       on_press=self.translate_text, size_hint=(None, None), size=(120, 48),
                                       pos_hint={'center_x': 0.5, 'center_y': 0.4})  # Positioned at the center
        self.text_output = TextInput(multiline=True, font_size='20sp', font_name='NotoSans-Regular.ttf', 
                                     hint_text='Translation will appear here...',
                                     size_hint=(0.8, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.15})  # Positioned near the bottom center

        # Add the UI elements to the layout
        layout.add_widget(self.listen_button)
        layout.add_widget(self.hindi_output)
        layout.add_widget(self.translate_button)
        layout.add_widget(self.text_output)

        return layout


    def listen_hindi(self, instance):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            audio = r.listen(source)

        try:
            print('Recognizing...')
            hindi_text = r.recognize_google(audio, language='hi-IN')
            # Add newlines and strip extra spaces from the recognized text
            hindi_text = hindi_text.strip().replace('.', '.\n\n')
            self.hindi_output.text = hindi_text
        except sr.UnknownValueError:
            print('Unable to recognize speech')
            self.hindi_output.text = "Unable to recognize speech. Please try again."
        except sr.RequestError as e:
            print(f'Request Error: {e}')
            self.hindi_output.text = "Speech recognition request failed. Please try again."

    def translate_text(self, instance):
        hindi_text = self.hindi_output.text
        if hindi_text.strip():
            # Translate Hindi text to English
            translator = Translator()
            translation = translator.translate(hindi_text, src='hi', dest='en')
            self.text_output.text = translation.text
        else:
            self.text_output.text = "Please speak in Hindi using the 'Listen' button first."

if __name__ == '__main__':
    MyApp().run()
