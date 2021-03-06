from typing import Set
from PIL import Image, ImageTk
from tkinter.ttk import Style, Progressbar, Combobox
from tkinter import messagebox
import tkinter
import time
import subprocess
import threading
import os
import webbrowser

import Utils
import Settings

threading.excepthook = Utils.thread_exceptions


class Progression(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent, bg='white')
        self.controller = controller
        self.max_workers = Settings.default_workers
        self.targets = []
        self.kill = False
        self.first_run = True
        self.kill_buttons = []
        self.execution_is_remote = False
        self.include_cmd_execution = True
        self.console_var = tkinter.StringVar(value="Show console")
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
            font=('Verdana', 7, 'underline'), bg='white'))
        log.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 7, ''), bg=Settings.bg_two))
        console = tkinter.Button(header, bg=Settings.bg_two, textvariable=self.console_var, relief='flat', bd=0,
            command=self.show_hide_console, fg=Settings.fg_one, cursor='hand2', font=('Verdana', 7), activebackground='white')
        console.grid(row=0, column=1, sticky='w', padx=3)
        console.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 7, 'underline'), bg='white'))
        console.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 7, ''), bg=Settings.bg_two))
        workers_input = tkinter.Entry(
            header, width=3, textvariable=self.workers_var, font=('Verdana', 7))
        workers_input.grid(row=0, column=3, sticky='e', padx=3)
        workers_label = tkinter.Label(header, bg=Settings.bg_two, text='Concurrent deployments:',
                                      relief='flat', bd=0, font=('Verdana', 7), fg=Settings.fg_one)
        workers_label.grid(row=0, column=2, sticky='e', padx=3)

        # Info and options
        info_label_frame = tkinter.Frame(self, bg='white')
        info_label_frame.grid(row=1, padx=10, sticky='news', pady=5)
        info_label_frame.grid_columnconfigure(1, weight=1)
        self.info_label = tkinter.Label(info_label_frame, bg='white', font=(
            'Verdana', 12), relief='flat', text='Initiate deployment')
        self.info_label.grid(row=0, column=0, sticky='w')
        self.verify_targets = tkinter.Button(info_label_frame, bg='white', text='Verify ping connections',
                                             state='disabled', relief='flat', bd=0, anchor='s', activebackground='white', fg=Settings.fg_one,
                                             command=lambda: threading.Thread(target=self.init_deployment, args=(False,), daemon=True).start(), font=('Verdana', 9))
        self.verify_targets.grid(row=0, column=1, sticky='e')
        self.kill_process_button = tkinter.Button(info_label_frame, bg='white', anchor='s', state='disabled',
                                                  text='Kill open processes', relief='flat', activebackground='white', bd=0,
                                                  command=lambda: threading.Thread(target=self.kill_running_targets, daemon=True).start(), font=('Verdana', 9))
        self.kill_process_button.grid(row=0, column=2, sticky='e')

        # Remote
        self.remote_frame = tkinter.Frame(self, bg=Settings.bg_one)
        self.remote_frame.grid(row=2, sticky='news', padx=10)
        self.remote_frame.columnconfigure(0, weight=3)
        self.remote_frame.columnconfigure(2, weight=1)
        self.remote_checkbutton = tkinter.Checkbutton(self.remote_frame, activebackground=Settings.bg_one,
                                                      text='Remote deployment', font=('Verdana', 8), relief='flat', variable=self.remote_var, fg=Settings.fg_one,
                                                      bg=Settings.bg_one, cursor='hand2', command=self.set_execution_type, bd=3, anchor='w', width=30)
        self.remote_checkbutton.grid(row=0, column=0, sticky='ew')
        self.remote_checkbutton.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 8, 'underline')))
        self.remote_checkbutton.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 8, '')))
        self.use_file_button = tkinter.Checkbutton(self.remote_frame, text=f'Use targets.txt', font=('Verdana', 8),
                                                   relief='flat', variable=self.use_file_var, fg=Settings.fg_one, bg=Settings.bg_one, cursor='hand2',
                                                   activebackground=Settings.bg_one, command=self.update_targets_field, bd=0, anchor='w')
        self.use_file_button.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 8, 'underline')))
        self.use_file_button.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 8, '')))
        self.select_computers_button = Combobox(
            self.remote_frame, textvariable=self.select_computers_var, justify='right', width=3)
        self.select_computers_button.config(values=list(sorted(set([line.strip("\n") for line in open(
            Settings.combobox_loc, "r") if len(line.strip("\n")) > 0]))), font=('Verdana', 7))
        self.select_computers_button.bind(
            '<<ComboboxSelected>>', lambda e: self.targets_text.insert("end", f";{self.select_computers_var.get()}"))
        self.targets_text = tkinter.Text(self.remote_frame, height=1, font=('Verdana', 9), bd=0, bg='white',
                                         fg='black', selectbackground='#ccd9e7', selectforeground='black', highlightthickness=0)

        # Deployment reports
        total_process_frame = tkinter.Frame(self, bg='white')
        total_process_frame.grid(row=3, sticky='news', padx=10)
        total_process_frame.grid_columnconfigure(0, weight=1)
        total_process_frame.grid_rowconfigure(0, weight=1)
        progression_canvas_frame = tkinter.Frame(total_process_frame, bg='white',
                                                 highlightthickness=2, highlightbackground=Settings.bg_one)
        progression_canvas_frame.grid(row=0, column=0, sticky="news")
        progression_canvas_frame.grid_columnconfigure(0, weight=1)
        progression_canvas_frame.grid_rowconfigure(0, weight=1)
        self.progression_canvas = tkinter.Canvas(progression_canvas_frame, bg='white',
                                                 scrollregion=(0, 0, 0, 0), highlightthickness=0)
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
        style.configure("green.Horizontal.TProgressbar", foreground=Settings.green_three, background=Settings.green_three,
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
        self.start_button = tkinter.Button(footer, bg='white', relief='flat', image=start_image, cursor='hand2',
                                           command=lambda: threading.Thread(target=self.init_deployment, daemon=True).start(), activebackground='white')
        self.start_button.grid(row=0, column=2, sticky='w')
        self.start_button.image = start_image

    def show_hide_console(self):
        if self.console_var.get() == "Show console":
            self.console_var.set("Hide console")
            Utils.cmd_visibility(show=True)
        else:
            self.console_var.set("Show console")
            Utils.cmd_visibility(show=False)

    def open_log(self):
        if os.path.exists(Settings.logfile):
            webbrowser.open(Settings.logfile)

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
            self.verify_targets.config(state='normal', font=(
                "Verdana", 9, ""), cursor='hand2')
            self.verify_targets.bind("<Enter>", lambda event: event.widget.config(
                font=('Verdana', 9, 'underline')))
            self.verify_targets.bind("<Leave>", lambda event: event.widget.config(
                font=('Verdana', 9, '')))
        else:
            self.targets_text.grid_remove()
            self.select_computers_button.grid_remove()
            self.use_file_button.grid_remove()
            self.use_file_var.set(0)
            self.verify_targets.config(
                state='disabled', cursor='arrow', font=("Verdana", 9, ""))
            self.verify_targets.unbind("<Enter>")
            self.verify_targets.unbind("<Leave>")

    def set_targets(self):
        if self.execution_is_remote:
            if self.use_file_var.get():
                self.targets = list(sorted(set([line.strip("\n") for line in open(
                    Settings.targets_loc, "r") if len(line.strip("\n")) > 0])))
            else:
                self.targets = [i for i in sorted(set(list(self.targets_text.get(
                    "1.0", "end").replace("\n", "").split(";")))) if len(i) > 0]
        else:
            self.targets = ['127.0.0.1']

    def create_cmd_file(self, cmd_location, sep='\n'):
        with open(cmd_location, 'w') as cmd:
            cmd.write(f'@echo off{sep}echo Starting time: %TIME%{sep}')
            if Settings.install_state == "Textinput":
                cmd.write(f"{Settings.text}{sep}")
            else:
                packages = Settings.installations if Settings.install_state == "Installation" else Settings.deletions
                for package in packages:
                    if packages[package][0].get():
                        cmd.write(
                            f"Echo @ {package}{sep}{packages[package][1]}{sep}")
                        cmd.write(
                            f"Echo ^> {Settings.install_state} of {package} ended with ErrorLevel: %ERRORLEVEL%{sep}")
            cmd.write(
                f"echo Final ErrorLevel: %ERRORLEVEL%{sep}echo Ending time: %TIME%")

    def decode(self, line):
        if b'\x00' in line and not b'\r' in line:
            return line.decode('utf-16-le', errors='ignore')
        else:
            return line.replace(b"\x00\r\x00", b"").decode('utf-8', errors='ignore')

    def init_target_deployment(self, hostname, status_name_, cmd_output_button, killbutton, connection,
                               errorlevel, runtime, cmd_output, n_targets):
        Settings.logger.info(f"INITIATED THREAD FOR {hostname}")
        cmd_location = os.path.join(Settings.temp_cmd_loc, f"{Settings.instance_uid}_{hostname}.cmd")
        start_time = time.time()
        height = 0
        lines = ""
        errorlevels = set()
        break_loop, logged_overflow = False, False

        # Verify ping connection
        pingable = Utils.pingable(
            hostname, Settings.test_pings) if self.execution_is_remote else True
        if not pingable:
            connection.config(text='X', fg=Settings.red_three)
            errorlevel.config(text="NO PING", fg=Settings.red_three)
        else:
            connection.config(text="???", fg=Settings.green_three)
            if not self.include_cmd_execution:
                errorlevel.config(text="NO ISSUE", fg=Settings.green_three)

        # Include execution and outputting of cmd/batch commands
        if self.include_cmd_execution and pingable and not self.kill:
            cmd_output_button.config(state='normal', cursor='hand2')
            cmd_output_button.bind("<Enter>", lambda event: event.widget.config(
                font=('Verdana', 9, 'underline')))
            cmd_output_button.bind("<Leave>", lambda event: event.widget.config(
                font=('Verdana', 9, '')))
            if n_targets == 1:
                cmd_output_button.invoke()

            # Init process
            cmd_location = os.path.join(Settings.temp_cmd_loc, f"{Settings.instance_uid}_{hostname}.cmd")
            self.create_cmd_file(cmd_location)
            cmd = [Settings.paexec_loc, f"\\\\{hostname}", "-f", "-s", "-c", "-csrc",
                   cmd_location, os.path.basename(cmd_location)]
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            # Killbutton config command
            killbutton.config(cursor='hand2', state='normal',
                              command=lambda: self.kill_target(hostname, process))
            killbutton.bind('<Enter>', Utils.lambdaf_event(
                Utils.obj_bg, status_name_, Settings.red_three), add="+")
            killbutton.bind('<Leave>', Utils.lambdaf_event(
                Utils.obj_bg, status_name_, Settings.bg_two), add="+")
            killbutton.bind("<Enter>", lambda event: event.widget.config(
                font=('Verdana', 9, 'underline')), add="+")
            killbutton.bind("<Leave>", lambda event: event.widget.config(
                font=('Verdana', 9, '')), add="+")

            # Start and read process
            read_line = time.time()
            for line in iter(process.stdout.readline, b''):
                read_line_delta = time.time() - read_line
                if self.kill:
                    self.kill_target(hostname, process)
                    break_loop = True

                # Decode line
                line = self.decode(line).rstrip()
                if len(line) < 1: continue
                if line.startswith("Ending time:"): break_loop = True
                if not errorlevel['text'] == 'ERROR' and 'ErrorLevel: ' in line:
                    lvl = line[line.index("ErrorLevel: ") +
                               len("ErrorLevel: "):]
                    if (lvl.lstrip('-').isdigit()) or lvl.isdigit():
                        errorlevels.add(int(lvl))
                        color, text = self.get_err_color_text(errorlevels)
                        errorlevel.config(text=text, fg=color)

                # Output insertion
                height += 1
                if height-1 <= Settings.max_output:
                    lines += f"{line}\n"
                    if not Settings.use_buffer or (height % Settings.buffersize == 0) or break_loop or\
                        read_line_delta > Settings.max_buffertime:
                        cmd_output.config(state='normal')
                        cmd_output.insert("end", lines)
                        if height <= Settings.max_output_height or n_targets == 1:
                            cmd_output.config(height=height)
                        cmd_output.config(state='disabled')
                        lines = ""
                else:
                    if not logged_overflow:
                        cmd_output.config(state='normal')
                        cmd_output.insert("end", f"Maximum output of {Settings.maxoutput} is reached")
                        cmd_output.config(state='disabled')
                        logged_overflow = True

                # New start time for calculating delta time
                read_line = time.time()
                if break_loop:
                    break

        # Unexpected shutdown
        if not break_loop and self.include_cmd_execution and pingable or self.kill:
            errorlevel.config(text='KILLED', fg=Settings.red_three)
            if len(lines.rstrip()) == 0:
                Settings.logger.error(f"UNEXPECTED SHUTDOWN FOR {hostname}")
            else:
                Settings.logger.error(f"UNEXPECTED SHUTDOWN FOR {hostname} WITH OUTPUT\n{lines.rstrip()}")

        # Finalize for target
        if os.path.exists(cmd_location):
            os.remove(cmd_location)
        cmd_output.config(state='normal')
        cmd_output.delete("end-1c linestart", "end")
        cmd_output.config(state='disabled')
        status_name_.config(bg=Settings.bg_two, fg=Settings.green_three)
        killbutton.unbind('<Enter>')
        killbutton.unbind('<Leave>')
        if errorlevel['text'] == 'RUNNING':
            errorlevel.config(text='UNKNOWN')
        killbutton.config(state='disabled', cursor='arrow',
                          font=("Verdana", 9, ""))
        runtime.config(text=time.strftime(
            "%H:%M:%S", time.gmtime(time.time()-start_time)))
        self.progressbar['value'] = self.progressbar['value'] + 1
        self.current_running_threads -= 1
        Settings.logger.info(
            f"TERMINATED THREAD FOR {hostname} WITH {height} READ LINES")

    def kill_running_targets(self):
        self.kill = True
        Settings.logger.info("KILL PROCESS FOR ALL TARGETS HAS BEEN INITIATED")
        self.kill_process_button.config(
            state='disabled', cursor='arrow', font=("Verdana", 9, ""))
        self.kill_process_button.unbind("<Enter>")
        self.kill_process_button.unbind("<Leave>")
        for button in self.kill_buttons:
            button.invoke()

    def kill_target(self, hostname, process):
        Settings.logger.info(f"KILL PROCESS HAS BEEN INITIATED FOR {hostname}")
        process.terminate()
        process.kill()
        killprocess = subprocess.Popen(['taskkill', '/S', hostname, '/F', '/T', '/IM', 'PAExec-*'],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(killprocess.stdout.readline, b''):
            line = self.decode(line).rstrip()
            if len(line) < 1:
                continue
            else:
                Settings.logger.info(line)

    def get_err_color_text(self, levels):
        color = Settings.green_three
        text = "NO ISSUE"
        for level in levels:
            if not level in [0, 1641, 3010]:
                return Settings.red_three, "ERROR"
            elif level in [1641, 3010]:
                color = 'orange'
                text = "REBOOT"
        return color, text

    def set_max_workers(self):
        input_workers = str(self.workers_var.get())
        if input_workers.isdigit() and int(input_workers) > 0:
            self.max_workers = int(input_workers)
        else:
            Settings.logger.error(
                "Max workers input is not a integer, or is lower than 1.")
            self.max_workers = Settings.default_workers

    def setup_canvas_frame(self):
        self.progression_frame = tkinter.Frame(
            self.progression_canvas, bg=Settings.bg_two)
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

    def exit_app(self):
        if Settings.running:
            if messagebox.askokcancel(title='Warning', message="Do you want to kill all running processes?"):
                t = threading.Thread(target=self.kill_running_targets, daemon=True)
                t.start()
                t.join()
                Settings.logger.info("ALL THREADS HAVE BEEN TERMINATED")
            else:
                return
        Utils.exit_app()

    def init_deployment(self, incl_execute=True):
        # Initialize and (re)set variables and fields
        if not self.first_run: self.progression_frame.destroy()
        self.kill = False
        self.first_run = False
        Settings.running = True
        self.kill_buttons = []
        self.include_cmd_execution = incl_execute
        self.execution_is_remote = self.remote_var.get()
        self.remote_checkbutton.config(
            state='disabled', font=("Verdana", 8, ""), cursor='arrow')
        self.remote_checkbutton.unbind("<Enter>")
        self.remote_checkbutton.unbind("<Leave>")
        self.kill_process_button.config(
            state='normal', font=("Verdana", 9, ""), cursor='hand2')
        self.kill_process_button.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 9, 'underline')))
        self.kill_process_button.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 9, '')))
        self.info_label.configure(text=Settings.install_state, fg='black')
        self.start_button.config(state="disabled", cursor='arrow')
        self.controller.protocol("WM_DELETE_WINDOW", lambda: threading.Thread(target=self.exit_app, daemon=True).start())
        self.verify_targets.config(
            state='disabled', cursor='arrow', font=("Verdana", 9, ""))
        self.verify_targets.unbind("<Enter>")
        self.verify_targets.unbind("<Leave>")
        self.set_targets()
        self.progressbar['value'] = 0
        self.progressbar['maximum'] = len(self.targets)
        self.current_running_threads = 0
        self.set_max_workers()
        self.setup_canvas_frame()

        # Create threads for all hostnames and wait for all threads to finish
        if len(self.targets) > 0:
            threads = []
            for hostname in self.targets:
                while self.current_running_threads >= self.max_workers:
                    time.sleep(0.5)
                if self.kill:
                    Settings.logger.info("STOPPED CREATING NEW TARGET FRAMES")
                    break
                self.current_running_threads += 1
                thread = threading.Thread(target=self.init_target_deployment,
                    args=self.create_targetframe(hostname))
                threads.append(thread)
                thread.start()
                self.progression_frame.update_idletasks()

        # Wait for all threads and end deployment
            for t in threads:
                t.join()
        self.deployment_finished()
        Settings.logger.info("ALL THREADS HAVE BEEN TERMINATED")

    def create_targetframe(self, hostname):
        status_frame = tkinter.Frame(
            self.progression_frame, bg=Settings.bg_two)
        status_frame.grid(sticky='news', padx=3, pady=3)
        status_frame.grid_columnconfigure(1, weight=1)
        status_frame.grid_rowconfigure(1, weight=1)
        output_button = tkinter.Button(status_frame, text="???", font=('Verdana', 9), bg=Settings.bg_two, relief='flat',
                                       bd=0, anchor='w', activebackground=Settings.bg_two, state='disabled', width=2)
        output_button.grid(row=0, column=0, sticky='ew', padx=3)
        cmd_output_frame = tkinter.Frame(status_frame)
        cmd_output_frame.grid_columnconfigure(0, weight=1)
        cmd_output = tkinter.Text(cmd_output_frame, font=('Verdana', 7), bg='white', bd=2,
                                  relief='sunken', state='disabled', height=0, highlightthickness=0,
                                  selectbackground=Settings.bg_one, selectforeground=Settings.fg_one)
        cmd_output.grid(row=0, column=0, sticky="nsew")
        cmd_output_scrollbar = tkinter.Scrollbar(cmd_output_frame, command=cmd_output.yview, bg=Settings.bg_two)
        cmd_output_scrollbar.grid(row=0, column=1, sticky="news")
        cmd_output.config(yscrollcommand=cmd_output_scrollbar.set)
        output_button.config(
            command=Utils.lambdaf(self.show_hide_cmd_output_frame, output_button, cmd_output_frame))
        status_name_frame = tkinter.Frame(status_frame, bg=Settings.bg_two)
        status_name_frame.grid(row=0, column=1, sticky='ew')
        status_name_frame.grid_columnconfigure(1, weight=1)
        status_name = tkinter.Label(status_name_frame, text="Name:", anchor='w',
                                    font=('Verdana', 9), bg=Settings.bg_two)
        status_name.grid(row=0, column=0, sticky='ew')
        status_name_ = tkinter.Label(status_name_frame, text=hostname, anchor='w', borderwidth=1, relief="flat",
                                     font=('Verdana', 9, 'bold'), bg=Settings.bg_two)
        status_name_.grid(row=0, column=1, sticky='ew')
        connection_frame = tkinter.Frame(status_frame, bg=Settings.bg_two)
        connection_frame.grid(row=0, column=4, sticky='ew')
        connection = tkinter.Label(
            connection_frame, text="Ping:", font=('Verdana', 9), bg=Settings.bg_two, anchor='w')
        connection.grid(row=0, column=1, sticky='ew')
        connection_ = tkinter.Label(connection_frame, font=('Verdana', 9, 'bold'), text='-',
                                    bg=Settings.bg_two, anchor='w', borderwidth=1, relief="flat", width=2)
        connection_.grid(row=0, column=2, sticky='ew')
        errorlevel_frame = tkinter.Frame(status_frame, bg=Settings.bg_two)
        errorlevel_frame.grid(row=0, column=3)
        errorlevel = tkinter.Label(
            errorlevel_frame, text="State:", font=('Verdana', 9), bg=Settings.bg_two, anchor='w')
        errorlevel.grid(row=0, column=0, sticky='ew')
        errorlevel_ = tkinter.Label(errorlevel_frame, text="RUNNING", font=('Verdana', 9, 'bold'),
                                    bg=Settings.bg_two, anchor='w', borderwidth=1, relief="flat", width=10)
        errorlevel_.grid(row=0, column=1, sticky='ew')
        runtime_frame = tkinter.Frame(status_frame, bg=Settings.bg_two)
        runtime_frame.grid(row=0, column=2, sticky='ew')
        runtime_frame.grid_columnconfigure(1, weight=1)
        runtime = tkinter.Label(
            runtime_frame, text="Runtime:", font=('Verdana', 9), bg=Settings.bg_two, anchor='e')
        runtime.grid(row=0, column=0, sticky='ew')
        runtime_ = tkinter.Label(runtime_frame,  font=('Verdana', 9, 'bold'), bg=Settings.bg_two, anchor='w',
                                 borderwidth=1, relief="flat", width=10, text='-')
        runtime_.grid(row=0, column=1, sticky='ew')
        killbutton = tkinter.Button(status_frame,  text="Kill", font=('Verdana', 9), bg=Settings.bg_two, anchor='e',
                                    relief="flat", activebackground=Settings.bg_two, bd=0, state='disabled', width=2)
        killbutton.grid(row=0, column=5, sticky='ew', padx=3)
        self.kill_buttons.append(killbutton)
        return (hostname, status_name_, output_button, killbutton, connection_,
            errorlevel_, runtime_, cmd_output, len(self.targets))

    def show_hide_cmd_output_frame(self, button, textframe):
        if button['text'] == "???":
            button.config(text="???")
            textframe.grid(row=1, sticky="news", pady=2, columnspan=7)
        else:
            button.config(text="???")
            textframe.grid_forget()

    def deployment_finished(self):
        Settings.running = False
        self.remote_checkbutton.config(
            state='normal', font=("Verdana", 8, ""), cursor='hand2')
        self.remote_checkbutton.bind("<Enter>", lambda event: event.widget.config(
            font=('Verdana', 8, 'underline')))
        self.remote_checkbutton.bind("<Leave>", lambda event: event.widget.config(
            font=('Verdana', 8, '')))
        self.kill_process_button.config(
            state='disabled', cursor='arrow', font=("Verdana", 9, ""))
        self.kill_process_button.unbind("<Enter>")
        self.kill_process_button.unbind("<Leave>")
        self.start_button.config(state='normal', cursor='hand2')
        if self.execution_is_remote:
            self.verify_targets.config(state='normal', font=(
                "Verdana", 9, ""), cursor='hand2')
            self.verify_targets.bind("<Enter>", lambda event: event.widget.config(
                font=('Verdana', 9, 'underline')))
            self.verify_targets.bind("<Leave>", lambda event: event.widget.config(
                font=('Verdana', 9, '')))
        self.progressbar['value'] = self.progressbar['maximum']
