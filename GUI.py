import tkinter, Cache
from tkinter import StringVar

class GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('OSRS')
        self.__build(self.root)


    def __build(self, root):
        self.input_box = tkinter.Entry(root)
        self.input_box.pack(padx=10, pady=10)

        self.search_btn = tkinter.Button(root)
        self.search_btn['text'] = "Search"
        self.search_btn['command'] = self.__search_btn_action
        self.search_btn.pack(padx=10, pady=10)

        self.label_stringvar = StringVar()
        self.num_results_label = tkinter.Label(textvariable=self.label_stringvar)
        self.num_results_label.pack()

        self.text_area = tkinter.Text(root, height=10, width=40)
        self.text_area.pack(padx=10, pady=10)


    def run(self):
        self.root.mainloop()


    def __search_btn_action(self):

        if self.input_box.get() == '':
            self.label_stringvar.set(F"({0} results found)")
            return

        results = Cache.search_ids(self.input_box.get())

        self.label_stringvar.set(F"({len(results)} results found)")

        for value in results:
            self.text_area.insert(tkinter.END, str(value['name']) + ' (' + str(value['id']) + ')' + '\n')
