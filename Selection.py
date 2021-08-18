from PIL import Image, ImageTk
import pandas
import tkinter
import math

import Utils
import Settings


class Selection(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent, bg="white")
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.prepare_data()
        self.powershell_var = tkinter.IntVar(self)

        ## Header ##
        header = tkinter.Frame(self, bg=Settings.bg_two)
        header.grid(row=0, sticky='new')
        texttocmd_button = tkinter.Button(header, bg=Settings.bg_two, font=('Verdana', 7), bd=0, text="Textinput",
                                          command=self.textfield_mode, cursor='hand2', relief='flat', activebackground='white')
        texttocmd_button.grid(row=0, column=0, sticky='news', padx=3)
        texttocmd_button.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 7, 'underline'), bg='white'))
        texttocmd_button.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 7, ''), bg=Settings.bg_two))
        deletion_button = tkinter.Button(header, bg=Settings.bg_two, font=('Verdana', 7), bd=0, text="Deletion",
                                         command=self.deletion_mode, cursor='hand2', relief='flat', activebackground='white')
        deletion_button.grid(row=0, column=1, sticky='news', padx=3)
        deletion_button.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 7, 'underline'), bg='white'))
        deletion_button.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 7, ''), bg=Settings.bg_two))
        installation_button = tkinter.Button(header, bg=Settings.bg_two, font=('Verdana', 7), bd=0, text="Installation",
                                             command=self.installation_mode, cursor='hand2', relief='flat', activebackground='white')
        installation_button.grid(row=0, column=2, sticky='news', padx=3)
        installation_button.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 7, 'underline'), bg='white'))
        installation_button.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 7, ''), bg=Settings.bg_two))

        ## Installation frame ##
        self.installation_frame = tkinter.Frame(self, bg='white')
        self.installation_frame.grid_columnconfigure(0, weight=1)
        self.installation_frame.grid_rowconfigure(1, weight=1)
        installation_header = tkinter.Frame(
            self.installation_frame, bg='white')
        installation_header.grid(row=0, sticky="news", pady=5)
        installation_header.grid_columnconfigure(0, weight=1)
        installation_info_label = tkinter.Label(installation_header, bg='white', font=(
            'Verdana', 12), relief='flat', text="Install software")
        installation_info_label.grid(row=0, column=0, sticky='w')
        self.selected_group = tkinter.StringVar(self, value='None')
        group_label = tkinter.Label(installation_header, bg='white', font=(
            'Verdana', 9), text="Softwaregroup: ", bd=0, anchor='e')
        group_label.grid(row=0, column=1, sticky='e')
        group_options = tkinter.OptionMenu(installation_header, self.selected_group,
                                           *self.software_groups, command=lambda e: self.apply_software_group())
        group_options.config(bg='white', activebackground='white', direction='left', font=(
            'Verdana', 9), anchor='e', indicatoron=0, cursor='hand2', bd=0, highlightthickness=0, activeforeground='black')
        group_options["menu"].config(bg='white', activebackground=Settings.bg_two, font=(
            'Verdana', 8), cursor='hand2', activeforeground='black')
        group_options.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 9, 'underline')))
        group_options.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 9, '')))
        group_options.grid(row=0, column=2, sticky='e')
        installation_button_frame = tkinter.Frame(
            self.installation_frame, highlightthickness=0, bd=0)
        installation_button_frame.grid(row=1, sticky="news")
        installation_button_frame.grid_columnconfigure(0, weight=1)
        installation_button_frame.grid_rowconfigure(0, weight=1)
        installation_canvas_frame = tkinter.Frame(installation_button_frame,
                                                  highlightthickness=2, highlightbackground=Settings.bg_one)
        installation_canvas_frame.grid(row=0, column=0, sticky="news")
        installation_canvas_frame.grid_columnconfigure(0, weight=1)
        installation_canvas_frame.grid_rowconfigure(0, weight=1)
        self.installation_canvas = tkinter.Canvas(
            installation_canvas_frame, bg="white", highlightthickness=0, scrollregion=(0, 0, 0, 0))
        self.installation_canvas.grid(row=0, column=0, sticky="news")
        installation_scrollbar_frame = tkinter.Frame(
            installation_button_frame, bd=0, highlightthickness=0)
        installation_scrollbar_frame.grid(row=0, column=1, sticky='news')
        installation_scrollbar_frame.grid_columnconfigure(0, weight=1)
        installation_scrollbar_frame.grid_rowconfigure(0, weight=1)
        installation_scrollbar_v = tkinter.Scrollbar(
            installation_scrollbar_frame, command=self.installation_canvas.yview)
        installation_scrollbar_v.grid(sticky='ns')
        self.installation_canvas.config(
            yscrollcommand=installation_scrollbar_v.set)

        ## Deletion frame ##
        self.deletion_frame = tkinter.Frame(self, bg='white')
        self.deletion_frame.grid_columnconfigure(0, weight=1)
        self.deletion_frame.grid_rowconfigure(1, weight=1)
        deletion_header = tkinter.Frame(self.deletion_frame, bg='white')
        deletion_header.grid(row=0, sticky="news", pady=5)
        deletion_header.grid_columnconfigure(0, weight=1)
        deletion_info_label = tkinter.Label(deletion_header, bg='white', font=(
            'Verdana', 12), relief='flat', text="Delete software")
        deletion_info_label.grid(row=0, column=0, sticky='w')
        deletion_button_frame = tkinter.Frame(
            self.deletion_frame, highlightthickness=0)
        deletion_button_frame.grid(row=1, sticky="news")
        deletion_button_frame.grid_columnconfigure(0, weight=1)
        deletion_button_frame.grid_rowconfigure(0, weight=1)
        deletion_canvas_frame = tkinter.Frame(deletion_button_frame,
                                              highlightthickness=2, highlightbackground=Settings.bg_one)
        deletion_canvas_frame.grid(row=0, column=0, sticky="news")
        deletion_canvas_frame.grid_columnconfigure(0, weight=1)
        deletion_canvas_frame.grid_rowconfigure(0, weight=1)
        self.deletion_canvas = tkinter.Canvas(
            deletion_canvas_frame, bg="white", highlightthickness=0, scrollregion=(0, 0, 0, 0))
        self.deletion_canvas.grid(row=0, column=0, sticky="news")
        deletion_scrollbar_frame = tkinter.Frame(deletion_button_frame)
        deletion_scrollbar_frame.grid(row=0, column=1, sticky='news')
        deletion_scrollbar_frame.grid_columnconfigure(0, weight=1)
        deletion_scrollbar_frame.grid_rowconfigure(0, weight=1)
        deletion_scrollbar_v = tkinter.Scrollbar(
            deletion_scrollbar_frame, command=self.deletion_canvas.yview)
        deletion_scrollbar_v.grid(sticky='ns')
        self.deletion_canvas.config(
            yscrollcommand=deletion_scrollbar_v.set)

        ## Textfield frame ##
        self.textfield_frame = tkinter.Frame(self, bg='white')
        self.textfield_frame.grid_columnconfigure(0, weight=1)
        self.textfield_frame.grid_rowconfigure(1, weight=1)
        textfield_header = tkinter.Frame(self.textfield_frame, bg='white')
        textfield_header.grid(row=0, sticky="news", pady=5)
        textfield_header.grid_columnconfigure(0, weight=1)
        info_label = tkinter.Label(textfield_header, bg='white', font=(
            'Verdana', 12), relief='flat', text="Text input to CMD/Powershell execution")
        info_label.grid(row=0, column=0, sticky='w')
        powershell_button = tkinter.Checkbutton(textfield_header, bg='white', activebackground="white", font=(
            'Verdana', 9), text="Powershell", bd=0, cursor='hand2', selectcolor='white', variable=self.powershell_var)
        powershell_button.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 9, 'underline')))
        powershell_button.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 9, '')))
        powershell_button.grid(row=0, column=2, sticky='e')
        textbox_frame = tkinter.Frame(
            self.textfield_frame, highlightthickness=0)
        textbox_frame.grid(row=1, sticky="news")
        textbox_frame.grid_columnconfigure(0, weight=1)
        textbox_frame.grid_rowconfigure(0, weight=1)
        textfield_input_frame = tkinter.Frame(textbox_frame,
                                              highlightthickness=2, highlightbackground=Settings.bg_one)
        textfield_input_frame.grid(row=0, column=0, sticky="news")
        textfield_input_frame.grid_columnconfigure(0, weight=1)
        textfield_input_frame.grid_rowconfigure(0, weight=1)
        self.textfield_input = tkinter.Text(textfield_input_frame, selectbackground=Settings.bg_two,
                                            selectforeground='black', state='normal', font=('Verdana', 9))
        self.textfield_input.grid(row=0, column=0, sticky="news")
        text_scrollbar_frame = tkinter.Frame(textbox_frame)
        text_scrollbar_frame.grid(row=0, column=1, sticky='news')
        text_scrollbar_frame.grid_columnconfigure(0, weight=1)
        text_scrollbar_frame.grid_rowconfigure(0, weight=1)
        text_scrollbar_v = tkinter.Scrollbar(
            text_scrollbar_frame, command=self.textfield_input.yview)
        text_scrollbar_v.grid(sticky='ns')
        self.textfield_input.config(
            yscrollcommand=text_scrollbar_v.set)

        # footer with buttons
        footer = tkinter.Frame(self, bg='white')
        footer.grid(row=2, sticky='news', padx=5, pady=5)
        footer.grid_columnconfigure(1, weight=1)
        clear_image = ImageTk.PhotoImage(Image.open(
            Settings.buttonclear).resize((50, 50), Image.ANTIALIAS))
        self.clear_button = tkinter.Button(footer, relief='flat', image=clear_image, bg='white', activebackground='white',
                                           command=lambda: self.remove_selections(Settings.installations), cursor='hand2')
        self.clear_button.grid(row=0, column=0, sticky='w')
        self.clear_button.image = clear_image
        mid_filler = tkinter.Label(footer, bg=Settings.bg_two)
        mid_filler.grid(row=0, column=1, sticky='ew', padx=5)
        proceed_image = ImageTk.PhotoImage(Image.open(
            Settings.buttonnext).resize((50, 50), Image.ANTIALIAS))
        proceed_button = tkinter.Button(footer, bg='white', relief='flat', image=proceed_image,
                                        cursor='hand2', command=self.intialize_progression, activebackground='white')
        proceed_button.grid(row=0, column=2, sticky='e')
        proceed_button.image = proceed_image

        # Init app
        self.place_checkbuttons(self.installation_canvas, self.installation_groups,
                                Settings.installations, Settings.green_one, Settings.green_two)
        self.place_checkbuttons(self.deletion_canvas, self.deletion_groups,
                                Settings.deletions, Settings.red_one, Settings.red_two)
        if Settings.start_frame.lower() == 'textinput':
            self.textfield_mode()
        elif Settings.start_frame.lower() == 'deletion':
            self.deletion_mode()
        else:
            self.installation_mode()

    def prepare_data(self):
        xlsx = pandas.read_excel(
            Settings.config_loc, sheet_name=None, header=None)
        software_names = xlsx['Software groups'].iloc[0][1:].to_list()
        self.software_groups = {cols.iloc[0]: [software_names[i] for i, v in enumerate(cols.iloc[1:]) if isinstance(
            v, str)] for _, cols in xlsx['Software groups'].iloc[1:].iterrows() if isinstance(cols.iloc[0], str)}
        self.installation_groups = xlsx["Installation groups"]\
            .rename(columns=xlsx["Installation groups"].iloc[0])\
            .drop(xlsx["Installation groups"].index[0])\
            .to_dict(orient='list')
        self.deletion_groups = xlsx["Deletion groups"]\
            .rename(columns=xlsx["Deletion groups"].iloc[0])\
            .drop(xlsx["Deletion groups"].index[0])\
            .to_dict(orient='list')
        self.installation_groups = {
            i: self.installation_groups[i] for i in self.installation_groups if isinstance(i, str)}
        self.deletion_groups = {
            i: self.deletion_groups[i] for i in self.deletion_groups if isinstance(i, str)}
        Settings.install_state = "Installation"
        Settings.installations = {cols.iloc[0]: (tkinter.IntVar(), cols.iloc[1])
                                  for _, cols in xlsx["Installations"].iterrows() if isinstance(cols.iloc[1], str)}
        Settings.deletions = {cols.iloc[0]: (tkinter.IntVar(), cols.iloc[1])
                              for _, cols in xlsx["Deletions"].iterrows() if isinstance(cols.iloc[1], str)}
        Settings.text = ""

    def select_group_software(self, valid_packages, packages, group_button_var):
        if group_button_var.get():
            group_button_var.set(0)
            for package in valid_packages:
                packages[package][0].set(0)
        else:
            group_button_var.set(1)
            for package in valid_packages:
                packages[package][0].set(1)

    def place_checkbuttons(self, canvas, groups, packages, select_color, hover_color):
        canvas.delete('all')
        main_frame = tkinter.Frame(canvas)
        main_frame.grid_columnconfigure(0, weight=1)
        for group in groups:
            valid_packages = list(
                filter(lambda p: p in packages, groups[group]))
            total_package_frame = tkinter.Frame(
                main_frame, bd=0, highlightthickness=0)
            total_package_frame.grid(sticky='news')
            total_package_frame.grid_columnconfigure(0, weight=1)
            group_button_var = tkinter.BooleanVar(value=False)
            group_button = tkinter.Button(total_package_frame, bg=Settings.bg_one, fg=Settings.fg_one,
                cursor='hand2', relief='flat', bd=0, highlightthickness=3, text=group, anchor='w',
                command=Utils.lambdaf(self.select_group_software, valid_packages, packages, group_button_var),
                font=('Verdana', 8), activebackground=Settings.bg_one)
            group_button.grid(sticky='news')
            group_button.bind("<Enter>", lambda event: event.widget.config(
                font=('Verdana', 8, 'underline')))
            group_button.bind("<Leave>", lambda event: event.widget.config(
                font=('Verdana', 8, '')))
            _textframe = tkinter.Frame(total_package_frame)
            _textframe.grid(sticky='news')
            _textframe.grid_propagate(0)
            _textframe.grid_columnconfigure(0, weight=1)
            package_frame = tkinter.Text(_textframe, bg='white', bd=0, highlightthickness=0,
                                         selectbackground='white', cursor='arrow')
            package_frame.grid(sticky='news')
            for package in valid_packages:
                _f = tkinter.Frame(package_frame, bg='white')
                checkbutton = tkinter.Checkbutton(_f, bg='white', text=package, bd=0, indicatoron=0, anchor='w',
                    highlightthickness=4, width=Settings.min_button_width, cursor='hand2',
                    variable=packages[package][0], relief='flat', font=('Verdana', 10), selectcolor=select_color)
                checkbutton.bind("<Enter>", lambda event: event.widget.config(
                    font=('Verdana', 10, 'underline'), bg=hover_color))
                checkbutton.bind("<Leave>", lambda event: event.widget.config(
                    font=('Verdana', 10, ''), bg='white'))
                checkbutton.grid(padx=2, pady=2, sticky='news')
                package_frame.window_create(tkinter.END, window=_f)
            package_frame.config(state='disabled')
            buttonwidth, buttonheight = checkbutton.winfo_reqwidth() + \
                5, checkbutton.winfo_reqheight()+5
            n_buttons = len(valid_packages)
            _textframe.bind("<Configure>", lambda e, n_buttons=n_buttons: self.adjust_text_height(
                e, buttonwidth, buttonheight, n_buttons))
        window = canvas.create_window((0, 0), window=main_frame, anchor='nw')
        canvas.bind('<Enter>', lambda e: canvas.bind_all(
            "<MouseWheel>", lambda e: Utils._on_mousewheel(e, canvas)))
        canvas.bind('<Leave>', lambda e: canvas.unbind_all("<MouseWheel>"))
        main_frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(
            window, width=e.width))

    def adjust_text_height(self, event, buttonwidth, buttonheight, n_buttons):
        newcols = max(1, event.widget.winfo_width()//buttonwidth)
        rows = math.ceil(n_buttons/newcols)
        event.widget.config(height=buttonheight*rows)

    def textfield_mode(self):
        self.deletion_frame.grid_forget()
        self.installation_frame.grid_forget()
        self.textfield_frame.grid(row=1, sticky='news', padx=10)
        self.clear_button.config(
            command=lambda: self.textfield_input.delete('1.0', tkinter.END))
        Settings.install_state = "Textinput"

    def deletion_mode(self):
        self.installation_frame.grid_forget()
        self.textfield_frame.grid_forget()
        self.deletion_frame.grid(row=1, sticky='news', padx=10)
        self.clear_button.config(
            command=lambda: self.remove_selections(Settings.deletions))
        Settings.install_state = "Deletion"

    def installation_mode(self):
        self.deletion_frame.grid_forget()
        self.textfield_frame.grid_forget()
        self.installation_frame.grid(row=1, sticky='news', padx=10)
        self.clear_button.config(
            command=lambda: self.remove_selections(Settings.installations))
        Settings.install_state = "Installation"

    def remove_selections(self, lib):
        for i in lib:
            lib[i][0].set(0)

    def apply_software_group(self):
        self.remove_selections(Settings.installations)
        for i in self.software_groups[self.selected_group.get()]:
            if i in Settings.installations:
                Settings.installations[i][0].set(1)

    def intialize_progression(self):
        if self.powershell_var.get():
            Settings.text = 'powershell -command "{}"'.format(
                self.textfield_input.get('1.0', tkinter.END).replace('\n', ';'))
        else:
            Settings.text = self.textfield_input.get("1.0", tkinter.END)
        self.controller.start_frame("Progression")
