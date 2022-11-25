import tkinter as tk

current_balance = 1000


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = {'Balance': tk.IntVar()}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MenuPage, WithdrawPage, BalancePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white')
        self.controller = controller

        self.controller.title('Банкомат')
        self.controller.state('zoomed')

        top_frame = tk.Frame(self, borderwidth=10, background='#228B22', height=200)
        top_frame.pack(fill='x', side='top')

        heading_label = tk.Label(self,
                                 text='Введите пин-код',
                                 font=('orbitron', 30, 'bold'),
                                 foreground='black',
                                 background='white',
                                 borderwidth=3)
        heading_label.pack(pady=0)
        my_password = tk.StringVar()
        password_entry_box = tk.Entry(self,
                                      textvariable=my_password,
                                      font=('orbitron', 12),
                                      width=22)
        password_entry_box.focus_set()
        password_entry_box.pack(ipady=7)

        def handle_focus_in(_):
            password_entry_box.configure(fg='black', show='*')

        password_entry_box.bind('<FocusIn>', handle_focus_in)

        count_pin = 3

        def check_password():
            if my_password.get() == '123':
                my_password.set('')
                incorrect_password_label['text'] = ''
                controller.show_frame('MenuPage')
            else:
                incorrect_password_label['text'] = 'Пароль введен неверно'

        password_label = tk.Label(self,
                                  text='Введите пин-код от вашей карты и нажмите ввод, либо заберите карту',
                                  font=('orbitron', 13),
                                  bg='white',
                                  fg='black')
        password_label.pack(pady=50)

        enter_button = tk.Button(self,
                                 text='Ввод',
                                 command=check_password,
                                 relief='flat',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        enter_button.pack(pady=10, anchor='e')

        incorrect_password_label = tk.Label(self,
                                            text='',
                                            font=('orbitron',13),
                                            fg='black',
                                            bg='white',
                                            anchor='n')
        incorrect_password_label.pack(fill='both', expand=True)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')


class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#228B22')
        self.controller = controller
   
        heading_label = tk.Label(self,
                                 background='#228B22')
        heading_label.pack(pady=50)

        main_menu_label = tk.Label(self,
                                   text='Выберите операцию для продолжения',
                                   font=('orbitron', 13),
                                   fg='black',
                                   bg='white')
        main_menu_label.pack(fill='x')

        button_frame = tk.Frame(self, bg='#FFFFFF')
        button_frame.pack(fill='both', expand=True)

        def balance():
            controller.show_frame('BalancePage')
            
        balance_button = tk.Button(button_frame,
                                    text='Просмотреть баланс на счете',
                                    command=balance,
                                    relief='flat',
                                    borderwidth=3,
                                    width=50,
                                    height=5)
        balance_button.pack(anchor='w', ipadx=10, ipady=10, pady=100)

        def withdraw():
            controller.show_frame('WithdrawPage')

        withdraw_button = tk.Button(button_frame,
                                    text='Снять наличные',
                                    command=withdraw,
                                    relief='flat',
                                    borderwidth=3,
                                    width=50,
                                    height=5)
        withdraw_button.pack(anchor='e', ipadx=10, ipady=10, pady=0)

        def exit():
            controller.show_frame('StartPage')
            
        exit_button = tk.Button(button_frame,
                                text='Забрать карту',
                                command=exit,
                                relief='flat',
                                borderwidth=3,
                                width=50,
                                height=5)
        exit_button.pack(anchor='sw', ipadx=10, ipady=10, pady=0)


class WithdrawPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white')
        self.controller = controller

        top_frame = tk.Frame(self, borderwidth=10, background='#228B22', height=200)
        top_frame.pack(fill='x', side='top')

        heading_label = tk.Label(self,
                                 background='white',
                                 fg='black',
                                 text='Введите сумму, которую хотите снять',
                                 font=('orbitron', 13))
        heading_label.pack(fill='x', pady=0)

        button_frame = tk.Frame(self, bg='white')
        button_frame.pack(fill='both', expand=True)

        cash = tk.StringVar()
        other_amount_entry = tk.Entry(button_frame,
                                      textvariable=cash,
                                      width=59,
                                      justify='right')
        other_amount_entry.pack(anchor='center', ipadx=10, ipady=10, pady=20)

        def other_amount(_):
            global current_balance
            if int(cash.get()) > current_balance:
                error_label['text'] = 'Недостаточно средств'
            else:
                current_balance -= int(cash.get())
                controller.shared_data['Balance'].set(current_balance)
                cash.set('')
                controller.show_frame('MenuPage')
            
        other_amount_entry.bind('<Return>', other_amount)

        error_label = tk.Label(self,
                               text='',
                               font=('orbitron', 13),
                               fg='black',
                               bg='white',
                               anchor='center')
        error_label.pack(fill='both', expand=True, side='top')

        enter_button = tk.Button(self,
                                 text='Ввод',
                                 relief='flat',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        enter_button.pack(pady=10, anchor='e')
        enter_button.bind('<Return>', other_amount)

        def back_main_menu():
            controller.show_frame('MenuPage')

        main_menu_button = tk.Button(button_frame,
                                text='Вернуться назад',
                                command=back_main_menu,
                                relief='flat',
                                borderwidth=3,
                                width=50,
                                height=5)
        main_menu_button.pack(anchor='w', ipadx=10, ipady=10, pady=50, side='bottom')


class BalancePage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#228B22')
        self.controller = controller

        top_frame = tk.Frame(self, borderwidth=10, background='#228B22', height=200)
        top_frame.pack(fill='x', side='top')

        global current_balance
        controller.shared_data['Balance'].set(current_balance)
        balance_label = tk.Label(self,
                                 textvariable=controller.shared_data['Balance'],
                                 font=('orbitron',13),
                                 fg='black',
                                 bg='white',
                                 anchor='center',
                                 height=5)
        balance_label.pack(fill='x')

        button_frame = tk.Frame(self, bg='white')
        button_frame.pack(fill='both', expand=True)

        def menu():
            controller.show_frame('MenuPage')
            
        menu_button = tk.Button(button_frame,
                                command=menu,
                                text='Вернуться назад',
                                relief='flat',
                                borderwidth=3,
                                width=50,
                                height=5)
        menu_button.pack(anchor='e', ipadx=10, ipady=10, pady=50, side='bottom')


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
