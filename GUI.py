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

        self.text_pad = tkst.ScrolledText(left_box, width=40, height=10)
        self.text_pad.pack(padx=10, pady=10)
        self.text_pad.configure(state=tk.DISABLED)

        right_box = tk.Frame(self.root)

        self.test_label = tk.Label(right_box, text="TEST").pack(padx=10, pady=10)

        left_box.pack(side="left")
        right_box.pack(side="right")

    def run(self):
        self.root.mainloop()


    def __search_btn_action(self):

        self.text_pad.configure(state=tk.NORMAL)
        self.text_pad.delete('1.0', tk.END)

        if self.input_box.get() == '':
            self.label_stringvar.set(F"({0} results found)")
            self.text_pad.configure(state=tk.DISABLED)
            return

        results = Cache.search_ids(self.input_box.get().strip())

        self.label_stringvar.set(F"({len(results)} results found)")

        for value in results:
            self.text_pad.insert(tk.INSERT, str(value['name']) + ' (' + str(value['id']) + ')' + '\n')

        self.text_pad.configure(state=tk.DISABLED)
