import tkinter as tk, Cache
from tkinter import StringVar
from pprint import pprint

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.update()
        self.root.minsize(600, 600)
        self.root.title('OSRS')
        self.__build()


    def __build(self):

        search_col = tk.Frame(self.root)

        tk.Label(search_col, text="Search for items").pack()

        self.input_box = tk.Entry(search_col)
        self.input_box.pack(padx=10, pady=10)

        tk.Button(search_col, text='Search', command=self.__search_btn_action)\
            .pack(padx=10, pady=10)

        self.label_stringvar = StringVar()
        tk.Label(search_col, textvariable=self.label_stringvar)\
            .pack()

        self.item_choices = tk.Listbox(search_col, width=60, height=20)
        self.item_choices.pack(padx=10, pady=10)
        self.item_choices.bind('<Double-1>', lambda x: self.__item_double_clicked())

        display_col = tk.Frame(self.root)

        self.name_str = StringVar()
        self.name_str.set('Test value')
        tk.Label(display_col, textvar=self.name_str).pack(pady=10, padx=20)

        canvas_width = canvas_height = 40
        self.item_icon = tk.Canvas(display_col, width=canvas_width, height=canvas_height)
        self.item_icon.pack(pady=(0,10), padx=10, side=tk.TOP)

        description_box = tk.Frame(display_col)
        tk.Label(description_box, text='Description:').pack(side=tk.LEFT)

        self.description_str = StringVar()
        self.description_str.set('Test Description')
        tk.Label(description_box, textvar=self.description_str, wraplength=150, justify=tk.LEFT).pack(padx=(0, 10),
                                                                                                      side=tk.LEFT)
        description_box.pack(side=tk.TOP, fill=tk.X)

        price_box = tk.Frame(display_col)
        tk.Label(price_box, text='Current Price:')\
            .pack(side=tk.LEFT)

        self.price_str = StringVar()
        self.price_str.set('Test price')
        tk.Label(price_box, textvar=self.price_str)\
            .pack(padx=(0,10), side=tk.LEFT)

        price_box.pack(side=tk.TOP, fill=tk.X)

        image = self.root.image = tk.PhotoImage(file='./cache/icon/thinking.gif')
        self.image_on_canvas = self.item_icon.create_image(canvas_width/2, canvas_height/2, anchor=tk.CENTER, image=image)


        search_col.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        display_col.pack(side=tk.LEFT, fill=tk.Y, padx=10)


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
            print(Cache.convert_to_double(data['current']['price']))

            image = self.root.image = tk.PhotoImage(file=Cache.get_cached_item_icon(itemID))
            self.item_icon.itemconfig(self.image_on_canvas, image=image)

            self.name_str.set(data['name'])
            self.price_str.set(data['current']['price'])
            self.description_str.set(data['description'])

    def __search_btn_action(self):

        self.item_choices.delete(0, tk.END)

        results = Cache.search_ids(self.input_box.get().strip())
        self.label_stringvar.set(F"({len(results)} results found)")

        for value in sorted([ str(value['name']) + ' (' + str(value['id']) + ')' + '\n' for value in results]):
            self.item_choices.insert(tk.END, value)
