from kivy.config import Config
from os.path import dirname, join,getsize, expanduser, getmtime
from os import *
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivymd.uix.spinner import MDSpinner
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivymd.toast import toast
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import BooleanProperty
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.button import *
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivy.animation import Animation
from kivy.network.urlrequest import *
from kivy.clock import Clock
from kivy.lang import Builder
from FirebaseFolder import firebase
from kivy.core.text import LabelBase
import subprocess,os, platform,json,threading,time,multitasking
from requests.exceptions import ConnectionError
import requests
from kivy.uix.modalview import ModalView

from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout

Window.size = (400,650)

Firebase = firebase.FirebaseApplication('https://bookme-1703626309990-default-rtdb.firebaseio.com/',None)
downloadsFolder = join('/storage/emulated/0/BookME', 'BookME') if platform == 'android' else (os.path.expanduser("~")+"/Downloads/BookME")

class SpinnerPopup(ModalView):
    pass

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()