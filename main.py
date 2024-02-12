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
from kivymd.uix.button import MDFlatButton,MDRaisedButton
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
#from configs import *

Window.size = (400,650)
Firebase = firebase.FirebaseApplication('https://bookme-1703626309990-default-rtdb.firebaseio.com/',None)
downloadsFolder = join('/storage/emulated/0', 'Download/BookME') if platform == 'android' else (os.path.expanduser("~")+"/Downloads/BookME")

#internal_storage_path = App.get_running_app().user_data_dir
class SpinnerPopup(ModalView):
    pass

class BookMe(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modal = None

    COLORS = {
        "RED" : (1,0,0,1),
        "GREEN" : (0,1,0,1),
        "BLUE" :(0,0,1,1),
        "LRED":(1,0,0,.5),
        "LGREEN" :(0,1,0,.5),
        "LBLUE": (0,0,1,.5),
        "PRI":(1,.65,0,1),
        "LPRI":(1,.65,0,.5),
        "LLPRI":(1,.65,0,.3)
    }
    isLoading = BooleanProperty(False)
       
    global screenManager
    global popup
    screenManager = ScreenManager()
    

    def on_start(self):
        try:
            os.mkdir(downloadsFolder)
        except Exception:
            pass
   
    @multitasking.task
    def downloadMe(self,downloadUrl,widget):
        try:
            widget.icon='progress-clock'
            widget.theme_text_color="Custom"
            widget.text_color=(0,.5,0,.5)
            req =  requests.get(downloadUrl, stream=True)
            filename = req.url[downloadUrl.rfind('/') + 1:]
            filename = join(downloadsFolder,filename)
            UrlRequest(downloadUrl,
                        on_progress=None,
                        #on_success=self.success(widget),
                        file_path=filename)
                
            widget.icon='progress-check'
            widget.theme_text_color="Custom"
            widget.text_color=self.COLORS['GREEN']
        except Exception as E:
            import traceback
            traceback.print_exc()
            widget.icon='progress-alert'
            widget.theme_text_color="Custom"
            widget.text_color=(1,0,0,1)            
                    
    def failure(self,widget):
        widget.icon='progress-alert'
        widget.theme_text_color="Custom"
        widget.text_color=(1,0,0,1)             
    
    def success(self,widget):
        widget.icon='progress-check'
        widget.theme_text_color="Custom"
        widget.text_color=(0,1,0,1)    
    
    def signup(self,email,username,password,nav):
        self.modal = SpinnerPopup()
        self.modal.open()
        try:
            if email != "" and username != "" and password != "":
                creds = {
                    "email":email,
                    "username":username,
                    "password":password
                }
                Firebase.post('bookme-1703626309990-default-rtdb/users',creds)
                nav.manager.transition.direction="left"
                nav.manager.current = "search"
                self.modal.dismiss()
                Snackbar(text="Account was created successfully!",
                        bg_color=self.COLORS['GREEN'],pos_hint={'center_x': .5, 'y': .75}).open()
            else :
                Snackbar(text="Fill in your details!",
                            bg_color=self.COLORS['LRED'],pos_hint={'center_x': .5, 'y': .75}).open()
                self.modal.dismiss()
        except ConnectionError:    
            Snackbar(text="Network problem was encountered!",
                            bg_color=self.COLORS['LRED'],pos_hint={'center_x': .5, 'y': .75}).open()
            self.modal.dismiss()
    
    def login(self, username, password,nav):
        self.modal = SpinnerPopup()
        self.modal.open()
        try:
            if username !='' and password !='':
                users = Firebase.get('bookme-1703626309990-default-rtdb/users','')
                for i in users.keys():
                    if username == users[i]['username'] and password == users[i]['password']:
                        userName = users[i]['username']
                        break
                    else:
                        userName = "Nul"
                    
                if userName !='Nul': 
                    nav.manager.transition.direction="left"
                    nav.manager.current = "search"
                    self.modal.dismiss()
                else:
                    Snackbar(text="Wrong username or password!",
                            bg_color=(1,0,0,1),pos_hint={'center_x': .5, 'y': .75}).open() 
                    self.modal.dismiss()
            else:
                Snackbar(text="Please Fill In Your Details!",
                        bg_color=(1,0,0,1),pos_hint={'center_x': .5, 'y': .75}).open() 
                self.modal.dismiss()
        except:    
            Snackbar(text="Something went wrong :( ",
                            bg_color=self.COLORS['LRED'],pos_hint={'center_x': .5, 'y': .75}).open()
            self.modal.dismiss()
    def nav(self,Nav,Direction):
        Nav.manager.transition.direction = Direction
        Nav.manager.current = "search"   
                
    def fetchBook(self,booktoSearch):
        self.modal.open()
        booktoSearch = booktoSearch.replace(' ','_')
        screenManager.get_screen("search").ids.box.clear_widgets()
        url = f"https://filepursuit.p.rapidapi.com/?q={booktoSearch}&filetype=pdf"
        from data import key,host
        headers = {
            "X-RapidAPI-Key": key,
            "X-RapidAPI-Host": host
        }
        #response = requests.get(url, headers=headers, params=querystring).json()
        response = UrlRequest(url, 
                            on_success=self.got_response,
                            req_headers=headers,
                            on_error=self.fail,
                            on_failure=self.fail,
                        )
                #Used dummy data for testing
        """ with open('response.json',mode='r') as file:
            response = json.load(file) """
            
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        
        screenManager.add_widget(Builder.load_file("Screens/main.kv"))
        screenManager.add_widget(Builder.load_file("Screens/login.kv"))
        screenManager.add_widget(Builder.load_file("Screens/signup.kv"))
        screenManager.add_widget(Builder.load_file("Screens/search.kv"))
        screenManager.add_widget(Builder.load_file("Screens/downloads.kv"))
        return screenManager
    
    def got_response(self, req, r):
        print(f'got response, {req.is_finished=}')
        response = r
        if response["status"] == "success":
                for result in response["files_found"]:
                    if result['file_size_bytes'] != "":
                        screenManager.get_screen("search").ids.box.add_widget(
                            MDExpansionPanel(                            
                            content=Builder.load_string(
f"""
MDBoxLayout:
    adaptive_height: True
    OneLineAvatarIconListItem:
        id:'lister'
        text: "Size : {result['file_size']}"
        theme_text_color: 'Custom'
        text_color: {self.COLORS['PRI']}

        IconLeftWidget:
            icon:'file-document-outline'
            theme_text_color: 'Custom'
            text_color: {self.COLORS['PRI']}
        
        IconRightWidget:
            icon:'progress-download'
            theme_text_color: 'Custom'
            text_color: {self.COLORS['BLUE']}
            on_release: app.downloadMe("{result['file_link']}",self)              
"""),
                            panel_cls=MDExpansionPanelThreeLine(
                                text=f"{result['file_name']}",
                                secondary_text=f"uploaded : {result['time_ago']}",
                                tertiary_text=f"source : {result['referrer_host']}",
                                theme_text_color='Custom',
                                text_color=(1,.65,0,1),
                                secondary_theme_text_color='Custom',
                                secondary_text_color=(1,.65,0,.5))
                            )
                        )
                self.modal.dismiss()                
        else :                      
            screenManager.get_screen("search").ids.box.clear_widgets()
            screenManager.get_screen("search").ids.box.add_widget(
    Builder.load_string(
    '''
    MDBoxLayout:
        orientation:'vertical'
        Image:
            source:'assets/icons/1.png'
            size_hint:1,None
    '''+f'''
        MDLabel:
            text: "RESPONSE : {response['status']} RECEIVED"
            font_name: 'assets/fonts/Lcd.ttf'
            font_size: "22sp"
            halign:"center"
            color: {self.COLORS['LRED']}
    ''')
    )                       
            self.modal.dismiss()

    def fail(self, req, r):
        self.modal.dismiss()
        screenManager.get_screen("search").ids.box.clear_widgets()
        screenManager.get_screen("search").ids.box.add_widget(
Builder.load_string(
'''
MDBoxLayout:
    orientation:'vertical'
    Image:
        source:'assets/icons/2.png'
        size_hint:1,None
'''+f'''
    MDLabel:
        text: "SOMETHING WENT WRONG"
        font_name: 'assets/fonts/Lcd.ttf'
        font_size: "22sp"
        halign:"center"
        color: {self.COLORS['LRED']}
''')
) 

    def on_downloads_active(self):
        #Clock.schedule_once(lambda x:self.showLoading('Fetching',True))
        try:
            os.mkdir(downloadsFolder)
        except Exception:
            pass
        screenManager.get_screen("downloads").ids.selection_list.clear_widgets()
        if listdir(downloadsFolder) ==[]:
            screenManager.get_screen("downloads").ids.selection_list.add_widget(
              Builder.load_string(
'''
MDBoxLayout:
    orientation:'vertical'
    spacing:"5dp"
    Image:
        source:'assets/icons/2.png'
        size_hint: 1, None
 
    MDLabel:     
        font_name: 'assets/fonts/Poppins-SemiBold.ttf'
        font_size: "25sp"
        text: "NO DOWNLOADS YET"
        halign:"center"
        color: app.COLORS['RED']
''')  
            )
            self.popup.dismiss()
        else:
            for File in listdir(downloadsFolder):
                name = File
                File = downloadsFolder+'/'+File
                size = getsize(File)
                Time = time.ctime(getmtime(File))
                intial_size = str(round(size/1024000,2)) +"MB" if int(size/1024000)!=0 else str(round(size/1024,2)) +"KB"
                
                #Logic to make the table
                screenManager.get_screen("downloads").ids.selection_list.add_widget(
                    Builder.load_string(
f"""
ThreeLineAvatarIconListItem:
    #on_release = 
    text: "{name}"
    secondary_text: "size : {intial_size}"
    tertiary_text:"Downloaded : {Time}"
    _no_ripple_effect: True
    theme_text_color:'Custom'
    text_color:(1,.65,0,1)
    secondary_theme_text_color:'Hint'
    tertiary_theme_text_color:'Custom'
    tertiary_text_color:(1,.65,0,.5)
    secondary_text_halign:'right'
    
    IconLeftWidget:
        icon:'file-document'
        theme_text_color: 'Custom'
        text_color: app.COLORS['LPRI']
        on_release: toast("Hello World", True, 80, 200, 0)
    
    IconRightWidget:
        icon:'arrow-top-right-thin-circle-outline'
        theme_text_color: 'Custom'
        text_color: app.COLORS['LGREEN']
        on_release: app.open_File("{File}")
"""
                    )
                )
    @multitasking.task
    def open_File(self,File):
        try:
            os.startfile(File)
        except AttributeError:
            subprocess.call(['open',File])
    
    def set_selection_mode(self, instance_selection_list, mode):
        if mode:
            md_bg_color = (0, 0, 0, 0)
            left_action_items = [["close",lambda x: screenManager.get_screen("downloads").ids.selection_list.unselected_all()]]
            right_action_items = [["trash-can-outline",lambda x : print("deleteFile")], ["share-variant"]]
        else:
            md_bg_color = (0, 0, 0, .01)
            left_action_items = [["chevron-up-circle-outline"]]
            right_action_items = [["magnify"], ["dots-vertical"]]
        screenManager.get_screen("downloads").ids.toolbar.title = "Downloads"
        #Animation(md_bg_color=(0, 0, 0, .01), d=0.2).start(screenManager.get_screen("downloads").ids.toolbar)
        screenManager.get_screen("downloads").ids.toolbar.left_action_items = left_action_items
        screenManager.get_screen("downloads").ids.toolbar.right_action_items = right_action_items
    
    def on_selected(self, instance_selection_list, instance_selection_item):
        screenManager.get_screen("downloads").ids.toolbar.title = str(
            len(instance_selection_list.get_selected_list_items())
        )
    
    def on_unselected(self, instance_selection_list, instance_selection_item):
        if instance_selection_list.get_selected_list_items():
            screenManager.get_screen("downloads").ids.toolbar.title = str(
                len(instance_selection_list.get_selected_list_items())
            )

    def deleteFile(self,instance_selection_list, instance_selection_item):
        print("STARTING>>>")

if __name__ == "__main__" :
    LabelBase.register(name="MPoppins",fn_regular="assets/fonts/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins",fn_regular="assets/fonts/Poppins-SemiBold.ttf")
    LabelBase.register(name="Bot",fn_regular="assets/fonts/Lcd.ttf")
    BookMe().run()
