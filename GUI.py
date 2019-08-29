import tkinter as tk, Cache
from tkinter import StringVar
from pprint import pprint

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

        self.item_choices = tk.Listbox(left_box, width=60, height=20)
        self.item_choices.pack(padx=10, pady=10)
        self.item_choices.bind('<Double-1>', lambda x: self.__item_double_clicked())

        right_box = tk.Frame(self.root)

        left_box.pack(side="left")
        right_box.pack(side="right")

    def run(self):
        self.root.mainloop()

    def __item_double_clicked(self):

        if self.item_choices.size() == 0:
            return

        selection = self.item_choices.get(self.item_choices.curselection())
        itemID = int(selection[selection.rfind('(')+1:selection.rfind(')')])

        data = Cache.get_cached_item(itemID)

        if data is not None:
            pprint(data)
            print(Cache.convert_to_double(data['item']['current']['price']))


    def __search_btn_action(self):

        self.item_choices.delete(0, tk.END)

        results = Cache.search_ids(self.input_box.get().strip())
        self.label_stringvar.set(F"({len(results)} results found)")

        for value in sorted([ str(value['name']) + ' (' + str(value['id']) + ')' + '\n' for value in results]):
            self.item_choices.insert(tk.END, value)
