from PIL import Image, ImageTk
from tkinter.ttk import Style, Progressbar, Combobox
import tkinter
import time
import subprocess
import threading
import os
import webbrowser

import Utils
import Settings


class Progression(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent, bg='white')
        self.controller = controller
        self.remote_var = tkinter.BooleanVar(value=False)
        self.message_var = tkinter.BooleanVar(value=False)
        self.use_file_var = tkinter.BooleanVar(value=False)
        self.workers_var = tkinter.StringVar(value=Settings.default_workers)
        self.select_computers_var = tkinter.StringVar()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Header
        header = tkinter.Frame(self, bg=Settings.bg_two)
        header.grid(row=0, sticky='news')
        header.grid_columnconfigure(1, weight=1)
        log = tkinter.Button(header, bg=Settings.bg_two, text='Open log', relief='flat', command=self.open_log,
                     fg=Settings.fg_one, cursor='hand2', font=('Verdana', 7), activebackground='white', bd=0)
        log.grid(row=0, column=0, sticky='w', padx=3)
        log.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 7, 'underline')))
        log.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 7, '')))
        workers_input = tkinter.Entry(
            header, width=3, textvariable=self.workers_var, font=('Verdana', 7))
        workers_input.grid(row=0, column=2, sticky='e', padx=3)
        workers_label = tkinter.Label(header, bg=Settings.bg_two, text='Concurrent deployments:',
                              relief='flat', bd=0, font=('Verdana', 7), fg=Settings.fg_one)
        workers_label.grid(row=0, column=1, sticky='e', padx=3)

        # Info and options
        info_label_frame = tkinter.Frame(self, bg='white')
        info_label_frame.grid(row=1, padx=10, sticky='news', pady=5)
        info_label_frame.grid_columnconfigure(1, weight=1)
        self.info_label = tkinter.Label(info_label_frame, bg='white', font=(
            'Verdana', 12), relief='flat', text='Initiate deployment')
        self.info_label.grid(row=0, column=0, sticky='w')
        self.verify_targets = tkinter.Button(info_label_frame, bg='white', text='Verify ping connections', state='disabled', relief='flat', bd=0, anchor='s', activebackground='white',
                                     fg=Settings.fg_one, command=lambda: threading.Thread(target=self.init_deployment, args=(False,)).start(), font=('Verdana', 9))
        self.verify_targets.grid(row=0, column=1, sticky='e')
        self.kill_process_button = tkinter.Button(info_label_frame, bg='white', anchor='s', state='disabled', text='Kill all processes', relief='flat', activebackground='white',
                                          bd=0, command=lambda: threading.Thread(target=self.kill_all_targets, daemon=True).start(), font=('Verdana', 9))
        self.kill_process_button.grid(row=0, column=2, sticky='e')

        # Remote
        self.remote_frame = tkinter.Frame(self, bg=Settings.bg_one)
        self.remote_frame.grid(row=2, sticky='news', padx=10)
        self.remote_frame.columnconfigure(0, weight=3)
        self.remote_frame.columnconfigure(2, weight=1)
        self.remote_checkbutton = tkinter.Checkbutton(self.remote_frame, activebackground=Settings.bg_one, text='Remote deployment', font=('Verdana', 8), relief='flat', variable=self.remote_var,
                                         fg=Settings.fg_one, bg=Settings.bg_one, cursor='hand2', command=self.set_execution_type, bd=3, anchor='w', width=30)
        self.remote_checkbutton.grid(row=0, column=0, sticky='ew')
        self.remote_checkbutton.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 8, 'underline')))
        self.remote_checkbutton.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 8, '')))
        self.use_file_button = tkinter.Checkbutton(self.remote_frame, text=f'Use targets.txt', font=('Verdana', 8), relief='flat', variable=self.use_file_var,
                                           fg=Settings.fg_one, bg=Settings.bg_one, cursor='hand2', activebackground=Settings.bg_one, command=self.update_targets_field, bd=0, anchor='w')
        self.use_file_button.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 8, 'underline')))
        self.use_file_button.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 8, '')))
        self.select_computers_button = Combobox(
            self.remote_frame, textvariable=self.select_computers_var, justify='right', width=3)
        self.select_computers_button.config(values=list(sorted(set([line.strip("\n") for line in open(
            Settings.combobox_loc, "r") if len(line.strip("\n")) > 0]))), font=('Verdana', 7))
        self.select_computers_button.bind(
            '<<ComboboxSelected>>', lambda e: self.targets_text.insert(tkinter.END, ";"+self.select_computers_var.get()))
        self.targets_text = tkinter.Text(self.remote_frame, height=1, font=('Verdana', 9), bd=0, bg='white',
                                 fg='black', selectbackground='#ccd9e7', selectforeground='black', highlightthickness=0)

        # Deployment reports
        total_process_frame = tkinter.Frame(self, bg='white')
        total_process_frame.grid(row=3, sticky='news', padx=10)
        total_process_frame.grid_columnconfigure(0, weight=1)
        total_process_frame.grid_rowconfigure(0, weight=1)
        progression_canvas_frame = tkinter.Frame(total_process_frame,
                                         highlightthickness=2, highlightbackground=Settings.bg_one, bg='white')
        progression_canvas_frame.grid(row=0, column=0, sticky="news")
        progression_canvas_frame.grid_columnconfigure(0, weight=1)
        progression_canvas_frame.grid_rowconfigure(0, weight=1)
        self.progression_canvas = tkinter.Canvas(
            progression_canvas_frame, bg="white", highlightthickness=0, scrollregion=(0, 0, 0, 0))
        self.progression_canvas.grid(row=0, column=0, sticky="news")
        progression_scrollbar_frame = tkinter.Frame(total_process_frame)
        progression_scrollbar_frame.grid(row=0, column=1, sticky='news')
        progression_scrollbar_frame.grid_columnconfigure(0, weight=1)
        progression_scrollbar_frame.grid_rowconfigure(0, weight=1)
        progression_scrollbar_v = tkinter.Scrollbar(
            progression_scrollbar_frame, command=self.progression_canvas.yview)
        progression_scrollbar_v.grid(sticky='ns')
        self.progression_canvas.config(
            yscrollcommand=progression_scrollbar_v.set)

        # footer
        footer = tkinter.Frame(self, bg='white')
        footer.grid(row=4, sticky='news', padx=5, pady=5)
        style = Style()
        style.theme_use('alt')
        style.configure("green.Horizontal.TProgressbar", foreground="#95d895", background="#95d895",
                        troughcolor=Settings.bg_two, thickness=19, highlightthickness=0, troughrelief='flat')
        self.progressbar = Progressbar(
            footer, style="green.Horizontal.TProgressbar", mode="determinate")
        self.progressbar.grid(row=0, column=1, padx=5, sticky='ew')
        footer.columnconfigure(1, weight=1)
        back_image = ImageTk.PhotoImage(Image.open(
            Settings.buttonback).resize((50, 50), Image.ANTIALIAS))
        back_button = tkinter.Button(footer, relief='flat', image=back_image, bg='white', activebackground='white',
                             command=lambda: controller.start_frame("Selection"), cursor='hand2')
        back_button.grid(row=0, column=0, sticky='w')
        back_button.image = back_image
        start_image = ImageTk.PhotoImage(Image.open(
            Settings.buttongo).resize((50, 50), Image.ANTIALIAS))
        self.start_button = tkinter.Button(footer, bg='white', relief='flat', image=start_image,
                                   cursor='hand2',  command=lambda: threading.Thread(target=self.init_deployment, daemon=True).start(), activebackground='white')
        self.start_button.grid(row=0, column=2, sticky='w')
        self.start_button.image = start_image

    def open_log(self):
        if os.path.exists(Settings.logs):
            webbrowser.open(Settings.logs)

    def update_targets_field(self):
        if self.use_file_var.get():
            self.targets_text.grid_remove()
        else:
            self.targets_text.grid(
                row=1, column=0, sticky='ew', padx=2, columnspan=3, pady=2)

    def set_execution_type(self):
        if self.remote_var.get():
            self.use_file_button.grid(row=0, column=1, sticky='e', padx=2)
            self.select_computers_button.grid(
                row=0, column=2, sticky='ew', padx=2)
            self.update_targets_field()
            self.verify_targets.config(state='normal', font=("Verdana", 9, ""), cursor='hand2')
            self.verify_targets.bind("<Enter>", lambda event: event.widget.config(
                font=('Verdana', 9, 'underline')))
            self.verify_targets.bind("<Leave>", lambda event: event.widget.config(
                font=('Verdana', 9, '')))
        else:
            self.targets_text.grid_remove()
            self.select_computers_button.grid_remove()
            self.use_file_button.grid_remove()
            self.use_file_var.set(0)
            self.verify_targets.config(state='disabled', cursor='arrow', font=("Verdana", 9, ""))
            self.verify_targets.unbind("<Enter>")
            self.verify_targets.unbind("<Leave>")

    def get_targets(self, remote):
        if remote:
            if self.use_file_var.get():
                return list(sorted(set([line.strip("\n") for line in open(
                    Settings.targets_loc, "r") if len(line.strip("\n")) > 0])))
            else:
                return [i for i in sorted(set(list(self.targets_text.get(
                    "1.0", tkinter.END).replace("\n", "").split(";")))) if len(i) > 0]
        else:
            return ['127.0.0.1']

    def create_cmd_file(self, sep='\n'):
        dir_name = os.path.dirname(Settings.temp_cmd_loc)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        with open(Settings.temp_cmd_loc, 'w') as cmd:
            cmd.write(f'@echo off{sep}echo Starting time:%TIME%{sep}')
            if Settings.install_state == "Textinput":
                cmd.write(Settings.text + sep)
            else:
                packages = Settings.installations if Settings.install_state == "Installation" else Settings.deletions
                for package in packages:
                    if packages[package][0].get():
                        cmd.write("Echo @ " + package + sep + packages[package][1] + sep)
                        cmd.write("Echo ^> {0} of {1} ended with ErrorLevel: %ERRORLEVEL%{2}".format(
                            Settings.install_state, package, sep))
            cmd.write(f"echo Final ErrorLevel: %ERRORLEVEL%{sep}echo Ending time:%TIME%") 

    def runtime(self, start_time):
        seconds = int(time.time() - start_time)
        if seconds < 61:
            return str(seconds) + ' sec'
        else:
            return str(seconds // 60) + ' min ' + str(seconds % 60) + ' sec'

    def psexec_command_for_file(self, remote, target):
        if remote:
            return f'{Settings.psexec_loc} \\\\{target} -n 10 -c -f -s -accepteula -nobanner {Settings.temp_cmd_loc}'
        else:
            return f"{Settings.psexec_loc} -c -f -s -accepteula -nobanner {Settings.temp_cmd_loc}"

    def remove_leading_whitespaces(self, line, chars):
        while len(line) > 0 and not line[0].lower() in chars:
            line = line[1:]
        return line

    def decode(self, line):
        chars = 'abcdefghijklmnpoqrstuvwxyz0123456789~`!@#$%^&*()_-+={}|[]\:";\'<>?,./'
        utf8 = self.remove_leading_whitespaces(
            line.decode(encoding='UTF-8', errors='ignore'), chars)
        if len(utf8) > 1 and not utf8[1].lower() in chars:
            if len(utf8) > 3 and not utf8[3].lower() in chars:
                return line.decode(encoding='UTF-16', errors='ignore') + "\n"
        return utf8

    def init_target_deployment(self, status_name_, output_button, killbutton, hostname, incl_execute, connection,
                        errorlevel, runtime, outputlabel, n_targets, remote):
        Settings.logger.info(f"INITIATED THREAD FOR: {hostname}")
        start_time = time.time()

        # Verify ping connection
        if remote and (not Utils.pingable(hostname, Settings.test_pings)):
            connection.config(text='X', fg="#b24531")
            errorlevel.config(text="NO PING", fg="#b24531")
        else:
            if remote:
                connection.config(text="✔", fg=Settings.suc_color)
                errorlevel.config(text="OKAY", fg=Settings.suc_color)

            # Include execution and outputting of Batch commands
            if incl_execute:
                output_button.config(state='normal', cursor='hand2')
                output_button.bind("<Enter>", lambda event: event.widget.config(
                    font=('Verdana', 9, 'underline')))
                output_button.bind("<Leave>", lambda event: event.widget.config(
                    font=('Verdana', 9, '')))
                if n_targets < 4 and not self.kill:
                    output_button.invoke()

                # Create process
                cmd = self.psexec_command_for_file(remote, hostname)
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                # Killbutton config command
                if self.kill:
                    self.kill_target(hostname, errorlevel, process)
                    self.target_finalization(status_name_, hostname, killbutton, start_time, runtime)
                    return
                killbutton.config(cursor='hand2', state='normal', command=lambda: threading.Thread(target=self.kill_target,
                    args=(hostname, errorlevel, process), daemon=True).start())
                self.killbuttons.append(killbutton)
                killbutton.bind('<Enter>', Utils.lambdaf_event(
                    Utils.obj_bg, status_name_, "#b24531"), add="+")
                killbutton.bind('<Leave>', Utils.lambdaf_event(
                    Utils.obj_bg, status_name_, Settings.bg_two), add="+")
                killbutton.bind("<Enter>", lambda event: event.widget.config(
                    font=('Verdana', 9, 'underline')), add="+")
                killbutton.bind("<Leave>", lambda event: event.widget.config(
                    font=('Verdana', 9, '')), add="+")

                # Start and read process
                height = 0
                errorlevels = set()

                while True:
                    time.sleep(0.08)
                    line = process.stdout.readline()

                    # End loop or skip line
                    if not line:
                        break
                    line = self.decode(line).rstrip()
                    if len(line) < 1:
                        continue

                    # Output parsing
                    if not errorlevel['text'] == 'ERROR' and 'ErrorLevel: ' in line:
                        lvl = line[line.index("ErrorLevel: ") + len("ErrorLevel: "):]
                        if (lvl[0] == '-' and lvl[1:].isdigit()) or lvl.isdigit():
                            errorlevels.add(int(lvl))
                            color, text = self.get_err_color_text(errorlevels)
                            errorlevel.config(text=text, fg=color)

                    # Output label insertion
                    height += 1
                    outputlabel.config(state='normal')
                    outputlabel.insert(tkinter.END, line + "\n")
                    if height <= Settings.max_output_length or n_targets == 1:
                        outputlabel.config(height=height)
                    outputlabel.config(state='disabled')

                    # End loop
                    if line.startswith("Ending time:") or height >= Settings.max_output:
                        break
                    if line.startswith('The handle is invalid')\
                            or line.startswith("De ingang is ongeldig"):
                        errorlevel.config(text="ERROR", fg="#b24531")
                        break

                # Delete last line with a newline
                outputlabel.config(state='normal')
                outputlabel.delete(f"{height+1}.0")
                outputlabel.config(state='disabled')

        # Finalize deployment
        self.target_finalization(status_name_, hostname, killbutton, start_time, runtime)

    def kill_all_targets(self):
        self.kill = True
        Settings.logger.info("KILL PROCESS HAS BEEN INITIATED")
        self.kill_process_button.config(state='disabled', cursor='arrow', font=("Verdana", 9, ""))
        self.kill_process_button.unbind("<Enter>")
        self.kill_process_button.unbind("<Leave>")
        for btn in self.killbuttons:
            btn.invoke()

    def kill_target(self, hostname, errorlevel, process):
        process.terminate()
        process.kill()
        killprocess = subprocess.Popen(['taskkill', '/S', hostname, '/F', '/T', '/IM', 'PSEXESVC.exe'],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            line = killprocess.stdout.readline()
            if not line:
                break
            line = self.decode(line).rstrip()
            if len(line) < 1:
                continue
            else:
                Settings.logger.info(line)
        errorlevel.config(text="KILLED", fg="#b24531")

    def target_finalization(self, status_name_, hostname, killbutton, start_time, runtime):
        status_name_.config(bg=Settings.bg_two, fg=Settings.suc_color)
        killbutton.unbind('<Enter>')
        killbutton.unbind('<Leave>')
        killbutton.config(state='disabled', cursor='arrow', font=("Verdana", 9, ""))
        runtime.config(text=self.runtime(start_time))
        self.progressbar['value'] = self.progressbar['value'] + 1
        self.current_running_threads -= 1
        Settings.logger.info(f"TERMINATED THREAD FOR: {hostname}")

    def get_err_color_text(self, levels):
        color = Settings.suc_color
        text = "OKAY"
        for level in levels:
            if not level in [0, 1641, 3010]:
                return "#b24531", "ERROR"
            elif level in [1641, 3010]:
                color = 'orange'
                text = "REBOOT"
        return color, text

    def get_max_workers(self):
        input_workers = str(self.workers_var.get())
        if input_workers.isdigit() and int(input_workers) > 0:
            return int(input_workers)
        else:
            return Settings.default_workers

    def create_canvas_contents(self):
        self.progression_frame = tkinter.Frame(self.progression_canvas, bg=Settings.bg_two)
        self.progression_frame.grid_columnconfigure(0, weight=1)
        self.progression_canvas.bind('<Enter>', lambda event: self.progression_canvas.bind_all(
            "<MouseWheel>", lambda e: Utils._on_mousewheel(e, self.progression_canvas)))
        self.progression_canvas.bind(
            '<Leave>', lambda e: self.progression_canvas.unbind_all("<MouseWheel>"))
        window = self.progression_canvas.create_window(
            (0, 0), window=self.progression_frame, anchor='nw')
        self.progression_frame.bind("<Configure>", lambda e: self.progression_canvas.configure(
            scrollregion=self.progression_canvas.bbox("all")))
        self.progression_canvas.bind(
            '<Configure>', lambda e: self.progression_canvas.itemconfig(window, width=e.width))
        self.progression_canvas.itemconfig(
            window, width=self.progression_canvas.winfo_width())

    def init_deployment(self, incl_execute=True):
        # Initialize and (re)set variables
        self.killbuttons = []
        self.kill = False
        self.remote_checkbutton.config(state='disabled', font=("Verdana", 8, ""), cursor='arrow')
        self.remote_checkbutton.unbind("<Enter>")
        self.remote_checkbutton.unbind("<Leave>")
        self.kill_process_button.config(state='normal', font=("Verdana", 9, ""), cursor='hand2')
        self.kill_process_button.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 9, 'underline')))
        self.kill_process_button.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 9, '')))
        self.progression_canvas.delete("all")
        self.progression_canvas.yview_moveto(0)
        self.info_label.configure(text=Settings.install_state, fg='black')
        self.start_button.config(state="disabled", cursor='arrow')
        self.controller.protocol("WM_DELETE_WINDOW", lambda: None)
        self.verify_targets.config(state='disabled', cursor='arrow', font=("Verdana", 9, ""))
        self.verify_targets.unbind("<Enter>")
        self.verify_targets.unbind("<Leave>")
        remote = self.remote_var.get()
        targets = self.get_targets(remote)
        self.progressbar['value'] = 0
        self.progressbar['maximum'] = len(targets)
        self.create_canvas_contents()
        self.create_cmd_file()
        self.current_running_threads = 0
        max_workers = self.get_max_workers()
        if len(targets) == 0:
            self.deployment_finished(remote=remote)
        
        # Submit processes for all hostnames
        threads = []
        for hostname in targets:
            while self.current_running_threads >= max_workers:
                time.sleep(0.05)
            if self.kill:
                Settings.logger.info("STOPPED CREATING NEW TARGET FRAMES")
                break
            self.current_running_threads += 1
            status_frame = tkinter.Frame(self.progression_frame, bg=Settings.bg_two, bd=4)
            output_button = tkinter.Button(status_frame, text="ᐁ", font=('Verdana', 9), bg=Settings.bg_two, relief='flat',
                                bd=0, anchor='w', activebackground=Settings.bg_two, state='disabled')
            output_button.grid(row=0, column=0, sticky='ew', padx=3)
            cmd_output = tkinter.Text(status_frame, font=(
                'Verdana', 7), bg='white', bd=2, relief='sunken', state='disabled', height=0)
            output_button.config(
                command=Utils.lambdaf(self.show_hide_cmd_output, output_button, cmd_output))
            status_name_frame = tkinter.Frame(status_frame, bg=Settings.bg_two)
            status_name_frame.grid(row=0, column=1, sticky='ew')
            status_name_frame.grid_columnconfigure(1, weight=1)
            status_name = tkinter.Label(status_name_frame, text="Name:", anchor='w',
                                font=('Verdana', 9), bg=Settings.bg_two)
            status_name.grid(row=0, column=0, sticky='ew')
            status_name_ = tkinter.Label(status_name_frame, text=hostname, anchor='w', borderwidth=1, relief="flat",
                                font=('Verdana', 9, 'bold'), bg=Settings.bg_two, width=8)
            status_name_.grid(row=0, column=1, sticky='ew')
            connection_frame = tkinter.Frame(status_frame, bg=Settings.bg_two)
            connection_frame.grid(row=0, column=3, sticky='ew')
            connection = tkinter.Label(
                connection_frame, text="Ping:", font=('Verdana', 9), bg=Settings.bg_two, anchor='w')
            connection.grid(row=0, column=1, sticky='ew')
            connection_ = tkinter.Label(
                connection_frame, font=('Verdana', 9, 'bold'), text='-', bg=Settings.bg_two, anchor='w', borderwidth=1, relief="flat", width=3)
            connection_.grid(row=0, column=2, sticky='ew')
            errorlevel_frame = tkinter.Frame(status_frame, bg=Settings.bg_two)
            errorlevel_frame.grid(row=0, column=4)
            
            errorlevel = tkinter.Label(
                errorlevel_frame, text="State:", font=('Verdana', 9), bg=Settings.bg_two, anchor='w')
            errorlevel.grid(row=0, column=0, sticky='ew')
            errorlevel_ = tkinter.Label(
                errorlevel_frame, text="RUNNING", font=('Verdana', 9, 'bold'), bg=Settings.bg_two, anchor='w', borderwidth=1, relief="flat", width=8)
            errorlevel_.grid(row=0, column=1, sticky='ew')
            runtime_frame = tkinter.Frame(status_frame, bg=Settings.bg_two)
            runtime_frame.grid(row=0, column=2, sticky='ew')
            runtime_frame.grid_columnconfigure(1, weight=1)
            runtime = tkinter.Label(
                runtime_frame, text="Runtime:", font=('Verdana', 9), bg=Settings.bg_two, anchor='e')
            runtime.grid(row=0, column=0, sticky='ew')
            runtime_ = tkinter.Label(runtime_frame,  font=('Verdana', 9, 'bold'), bg=Settings.bg_two, anchor='w',
                borderwidth=1, relief="flat", width=3, text='-', fg=Settings.suc_color)
            runtime_.grid(row=0, column=1, sticky='ew')
            killbutton = tkinter.Button(status_frame,  text="Kill", font=('Verdana', 9), bg=Settings.bg_two, anchor='e',
                        relief="flat", activebackground=Settings.bg_two, bd=0, state='disabled', width=3)
            killbutton.grid(row=0, column=5, sticky='ew')
            status_frame.grid(sticky='news', padx=2, pady=2)
            status_frame.grid_columnconfigure(1, weight=5)
            status_frame.grid_columnconfigure(2, weight=1)
            t = threading.Thread( target=self.init_target_deployment, args=(status_name_, output_button, killbutton, hostname,
                            incl_execute, connection_, errorlevel_, runtime_, cmd_output, len(targets), remote), daemon=True)
            threads.append(t)
            t.start()
            time.sleep(0.05)
        
        # Wait for all threads and finalize
        for t in threads:
            t.join()
        self.deployment_finished(remote=remote)
        Settings.logger.info("ALL THREADS HAVE BEEN TERMINATED")

    def show_hide_cmd_output(self, button, text):
        if button['text'] == "ᐁ":
            button.config(text="ᐃ")
            text.grid(row=1, sticky="news", columnspan=7, pady=2)
        else:
            button.config(text="ᐁ")
            text.grid_forget()

    def deployment_finished(self, remote):
        self.remote_checkbutton.config(state='normal', font=("Verdana", 8, ""), cursor='hand2')
        self.remote_checkbutton.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 8, 'underline')))
        self.remote_checkbutton.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 8, '')))
        self.kill_process_button.config(state='disabled', cursor='arrow', font=("Verdana", 9, ""))
        self.kill_process_button.unbind("<Enter>")
        self.kill_process_button.unbind("<Leave>")
        self.start_button.config(state='normal', cursor='hand2')
        if remote:
            self.verify_targets.config(state='normal', font=("Verdana", 9, ""), cursor='hand2')
            self.verify_targets.bind("<Enter>", lambda event: event.widget.config(
                font=('Verdana', 9, 'underline')))
            self.verify_targets.bind("<Leave>", lambda event: event.widget.config(
                font=('Verdana', 9, '')))
        self.controller.protocol("WM_DELETE_WINDOW", Utils.exit_app)
        self.progressbar['value'] = self.progressbar['maximum']
