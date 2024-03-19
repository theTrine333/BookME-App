from _inits import *

class BookMe(MDApp):
    Poster = StringProperty()
    Title = StringProperty()
    Info = StringProperty()
    FileType = StringProperty()
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
    global screenManager
    screenManager = ScreenManager()

    def on_start(self):                  
        if platform == 'android':
            from android.permissions import Permssion,request_permissions
            request_permissions([Permssion.READ_EXTERNAL_STORAGE,Permssion.WRITE_EXTERNAL_STORAGE,Permssion.MANAGE_EXTERNAL_STORAGE])
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
            if email != '' and username != '' and password != '':
                creds = {"email":email,"username":username,"password":password}
                Firebase.post('bookme-1703626309990-default-rtdb/users',creds)
                nav.manager.transition.direction="left"
                nav.manager.current = "search"
                self.modal.dismiss()
                Snackbar(text="Account was created successfully!",
                        bg_color=self.COLORS['GREEN'],pos_hint={'center_x': .5, 'y': .75}).open()
            else :
                text = 'Fill in your details in order to Signup'
                self.dialog = MDDialog(
                    text=text,
                    cls = self.theme_cls.primary_palette,
                    auto_dismiss=False,
                    type='alert',
                    radius=[20, 7, 20, 7],
                    buttons=[
                        MDRaisedButton(
                            text="Close",
                            on_release = (lambda x : self.dialog.dismiss())
                        ),
                    ],
                )
                self.dialog.open()
                self.modal.dismiss()
        except:    
            text = 'An error has occured, please try again later. If the error persists please contact the developers for help and guidance'
            self.dialog = MDDialog(
                text=text,
                cls = self.theme_cls.primary_palette,
                auto_dismiss=False,
                type='alert',
                radius=[20, 7, 20, 7],
                buttons=[
                    MDRaisedButton(
                        text="Close",
                        on_release = (lambda x : self.dialog.dismiss())
                    ),
                ],
            )
            self.modal.dismiss()
    def login(self, nav):
        self.modal = SpinnerPopup()
        self.modal.open()
        try:
            username = screenManager.get_screen('login').ids.usename_field.text
            password = screenManager.get_screen('login').ids.passwd_field.text
            
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
                self.modal.dismiss()
                text = 'Fill in your details to Signin'
                self.dialog = MDDialog(
                    text=text,
                    cls = self.theme_cls.primary_palette,
                    auto_dismiss=False,
                    type='alert',
                    radius=[20, 7, 20, 7],
                    buttons=[
                        MDRaisedButton(
                            text="Close",
                            on_release = (lambda x : self.dialog.dismiss())
                        ),
                    ],
                )
                self.dialog.open()

        except:    
            Snackbar(text="Something went wrong :( ",
                            bg_color=self.COLORS['LRED'],pos_hint={'center_x': .5, 'y': .75}).open()
            self.modal.dismiss()
    def nav(self,Nav,Direction):
        Nav.manager.transition.direction = Direction
        Nav.manager.current = "search"   
                
    def setDetails(self,url,fileType):
        book_details = getBookDetails(url)
        self.Poster = book_details[0][1]
        self.Title = book_details[0][0]
        self.Link = book_details[0][2]
        self.FileType = fileType
        try:
            self.Info = book_details[0][3]
        except:
            self.Info = "Unknown"
    def fetchBook(self,booktoSearch):
        self.modal = SpinnerPopup()
        self.modal.open()
        booktoSearch = booktoSearch.replace(' ','_')
        screenManager.get_screen("search").ids.box.clear_widgets()
        try:
            results = searchBooks(booktoSearch)
            if results !=[]:
                for result in results:
                    #bookTitle = result[0]
                    #lastIndex = bookTitle.rfind(":")
                    #self.bookTitle = bookTitle[::lastIndex+1]
                    #print(self.bookTitle)
                    if result[3] =="pdf":
                        screenManager.get_screen("search").ids.box.add_widget(
                            MDExpansionPanel(                            
                                content=Builder.load_string(
    f"""
MDBoxLayout:
    adaptive_height: True
    OneLineAvatarIconListItem:
        id:'lister'
        text: "Size : {result[2]}"
        theme_text_color: 'Custom'
        text_color: {self.COLORS['PRI']}

        IconLeftWidget:
            icon:'file-document-outline'
            theme_text_color: 'Custom'
            text_color: {self.COLORS['PRI']}
        
        IconRightWidget:
            icon:'arrow-right-circle-outline'
            theme_text_color: 'Custom'
            text_color: {self.COLORS['PRI']}
            on_release: 
                #app.screenManager.transition.direction="left"
                app.root.current = "about"
                app.setDetails("{result[1]}","{result[3]}")
                                
    """),
                                panel_cls=MDExpansionPanelTwoLine(
                                    text=f"{result[0]}",
                                    secondary_text=f"Language : {result[4]}",
                                    theme_text_color='Custom',
                                    text_color=(1,.65,0,1),
                                    secondary_theme_text_color='Custom',
                                    secondary_text_color=(1,.65,0,.5))
                                )
                            )
                
                self.modal.dismiss()
            else:
                self.dialog = MDDialog(
                    text="No results found",
                    cls = self.theme_cls.primary_palette,
                    auto_dismiss=False,
                    type='alert',
                    radius=[7, 7, 7, 7],
                    buttons=[
                        MDRaisedButton(
                            text="Close",
                            on_release = (lambda x : self.dialog.dismiss())
                        ),
                    ],
                )
                self.dialog.open()
                self.modal.dismiss()
        except:
            self.dialog = MDDialog(
                    title="Error Occured",
                    text="Something went wrong\nDo you wish to try again?",
                    cls = self.theme_cls.primary_palette,
                    auto_dismiss=False,
                    type='alert',
                    radius=[7, 7, 7, 7],
                    buttons=[
                        MDRaisedButton(
                            text="Close",
                            on_release = (lambda x : self.dialog.dismiss())
                        ),
                        MDRaisedButton(
                            text="Retry",
                            on_release =lambda x : (
                                self.dialog.dismiss(),
                                self.fetchBook(booktoSearch)
                            )
                        )
                    ],
                )
            
            self.dialog.open()
            self.modal.dismiss()
           
    def start_download(self, url):
        self.modal = SpinnerPopup()
        self.modal.open()
        # URL pointing directly to the image file
        self.request = UrlRequest(
            url, 
            on_progress=self.on_progress, 
            on_error=self.on_error,
            on_success=self.on_success_download,
            chunk_size=1024,
            file_path=f"{downloadsFolder}\\{self.Title}.{self.FileType}"
        )
        self.modal.dismiss()

    def on_progress(self, request, current_size, total_size):
        if total_size and current_size:
            progress = int((current_size / total_size) * 100)
            screenManager.get_screen("about").ids.progress_bar.value = progress
            #self.progress_bar.value = progress
    
        
    def on_success_download(self, request, result):
        screenManager.get_screen("about").ids.progress_bar.value = 0
        notification.notify(
            app_name = "BookME",
            #app_icon = "/assets/icons/0.png",
            title = "BookME",
            message="Download completed successfully" ,
            # displaying time
            timeout=2
        )

    def on_error(self, request, error):
        screenManager.get_screen("about").ids.progress_bar.value = 0
        print("Download error:", error)
            
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        
        screenManager.add_widget(Builder.load_file("Screens/main.kv"))
        #screenManager.add_widget(Builder.load_file("Screens/login.kv"))
        screenManager.add_widget(Builder.load_file("Screens/about.kv"))
        screenManager.add_widget(Builder.load_file("Screens/signup.kv"))
        screenManager.add_widget(Builder.load_file("Screens/search.kv"))
        screenManager.add_widget(Builder.load_file("Screens/downloads.kv"))
        return screenManager
    def on_downloads_active(self):
        try:
            os.mkdir(downloadsFolder)
        except Exception:
            pass
        screenManager.get_screen("downloads").ids.selection_list.clear_widgets()
        if listdir(downloadsFolder) == []:
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
                File = downloadsFolder+'\\'+File
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


if __name__ == "__main__" :
    LabelBase.register(name="MPoppins",fn_regular="assets/fonts/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins",fn_regular="assets/fonts/Poppins-SemiBold.ttf")
    LabelBase.register(name="Bot",fn_regular="assets/fonts/Lcd.ttf")
    BookMe().run()
