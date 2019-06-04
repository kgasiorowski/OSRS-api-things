import tkinter as tk, Cache
import tkinter.scrolledtext as tkst
from tkinter import StringVar

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('OSRS')
        self.__build()


    def __build(self):

        left_box = tk.Frame(self.root)

        self.input_box = tk.Entry(left_box)
        self.input_box.pack(padx=10, pady=10)

        self.search_btn = tk.Button(left_box)
        self.search_btn['text'] = "Search"
        self.search_btn['command'] = self.__search_btn_action
        self.search_btn.pack(padx=10, pady=10)

        self.label_stringvar = StringVar()
        self.num_results_label = tk.Label(left_box, textvariable=self.label_stringvar)
        self.num_results_label.pack()

        # self.text_pad = tkst.ScrolledText(left_box, width=40, height=10)
        # self.text_pad.pack(padx=10, pady=10)
        # self.text_pad.configure(state=tk.DISABLED)

        self.item_choices = tk.Listbox(left_box, width=60, height=20)
        self.item_choices.pack(padx=10, pady=10)

        right_box = tk.Frame(self.root)

        left_box.pack(side="left")
        right_box.pack(side="right")

    def run(self):
        self.root.mainloop()


    def __search_btn_action(self):

        self.item_choices.delete(0, tk.END)

        if self.input_box.get() == '':
            self.label_stringvar.set(F"({0} results found)")
            return

        results = Cache.search_ids(self.input_box.get().strip())

        self.label_stringvar.set(F"({len(results)} results found)")

        for value in results:
            self.item_choices.insert(tk.END, str(value['name']) + ' (' + str(value['id']) + ')' + '\n')

        pass