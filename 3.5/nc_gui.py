# https://docs.python.org/3/library/tkinter.html
from tkinter import *
# https://docs.python.org/3/library/tkinter.ttk.html
from tkinter import ttk
# https://www.tutorialspoint.com/python3/tk_messagebox.htm
from tkinter import messagebox
import time
import nightcrawler as NC

"""
@author: neolace
@date: 2022-06-28

Tkinter Documentation:
http://knowpapa.com/ttk-treeview/
https://docs.python.org/2/library/tkinter.html
"""

class Gui_Crawler(NC.Crawler):
    """
    """

    def start(self, tree=None):
        """
            Trigger function that starts to fetch links from self.base_url
        """

        time_start = time.time()
        print('Please stand by ...\n')
        print('BASE URL: {0}'.format(self.base_url))

        # This variable is my index for the list of child links
        # we are going to analize child by child until there
        # are no more new childs
        i = 0

        while i < len(self.CHILD_LINKS):
            if i:
                tree.insert('', 'end', '', text=self.CHILD_LINKS[i])
            self.map_files(self.CHILD_LINKS[i])
            i += 1

        print()
        print('-'*32)
        print('Results:')
        print('{0:d} email accounts, {1:d} tel. numbers and {2:d} links' \
              '({3:6f} seconds) ... \n'.format(len(self.EMAIL_ACCOUNTS), len(self.TEL_NUMS),
                                          len(self.CHILD_LINKS), time.time() - time_start))
        print('Links:')
        print(self.CHILD_LINKS)
        print('Emails:')
        print(self.EMAIL_ACCOUNTS)
        print('T:')
        print(self.TEL_NUMS)

class MainWindow(Frame):
    def __init__(self, master=None):
        # Master frame
        master.minsize(width=768, height=400)
        master.title("NightCrawler: Web Scraper v{0}".format(NC.VERSION))
        Frame.__init__(self, master)
        self.pack()

        # Widgets
        self.add_widgets()
        self.parent_nodes = ["/index.php", "/css/estilos.css",
                             "/admin/index.php", "/about.php"]

    def start_c(self, txt_domain, tree):
        tmp_domain = txt_domain.get().strip()
        if not tmp_domain:
            messagebox.showwarning("Empty Domain",
                                     "Please introduce a valid domain address" \
                                     "\nE.g.: http://valid_domain")
            txt_domain.focus_set()
            return

        crawler = Gui_Crawler(tmp_domain)
        try:
            crawler.start(tree)
        except Exception as e:
            messagebox.showerror("Wrong Domain Address",
                                   "Please introduce a valid address\n" \
                                   "E.g.: http://valid_domain"
                                   "\n\nError MSG: {0}".format(e))


    def add_widgets(self):
        # Txt box
        txt_domain = Entry(self, width=50)
        txt_domain.pack()
        txt_domain.focus_set()

        # Tree container
        tree = MyTree(self)
        tree.configure(columns=("status",))
        tree.column("status", width=100)
        tree.heading("status", text="Status")

        # Button start
        btn_start = Button(self, text="Start", width=10,
                           command=lambda: self.start_c(txt_domain, tree))
        btn_start.pack()

        tree.pack()

    def create_tree(self):
        tree = ttk.Treeview(self)
        tree.pack()

        # Inserted at the root, program chooses id:
        tree.insert('', 'end', 'widgets', text='Widget Tour')

        # Same thing, but inserted as first child:
        tree.insert('', 0, 'gallery', text='Applications')

        # Treeview chooses the id:
        my_id = tree.insert('', 'end', text='Tutorial')
        # Inserted underneath an existing node:
        tree.insert('widgets', 'end', text='Canvas')

        tree.insert(my_id, 'end', text='Tree')

        tree.insert('', 2,text="Ouw!")


class MyTree(ttk.Treeview):
    def __init__(self, parent):
        ttk.Treeview.__init__(self, parent)

    def insert(self, *args, **kwargs):

        try:
            node_children = self.get_children("widgets")
        except:
            node_children = []

        res = ttk.Treeview.insert(self, *args, **kwargs)
        print(node_children)

        return res



if __name__ == '__main__':
    root = Tk()
    main_window = MainWindow(master=root)
    root.mainloop()
    try:
        root.destroy()
    except TclError:
        print("Exit :)")
