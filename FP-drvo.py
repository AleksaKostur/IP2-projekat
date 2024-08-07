# Uvoz potrebnih biblioteka
import pyfpgrowth
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from collections import defaultdict


# Definisanje globalne promenljive za figuru
global fig
fig = None


def load_transactions(transactions_text):
    
    filepath = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not filepath:
        return
    
    with open(filepath, 'r') as file:
        transactions_text.delete('1.0', tk.END)
        transactions_text.insert(tk.END, file.read())


# Definicija čvora FP-drveta
class TreeNode:
    def __init__(self, name, count, parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.children = {}
        self.link = None


# Dodavanje transakcije u FP-drvo
def add_transaction(tree, transaction, header_table, count):
    
    if transaction[0] in tree.children:
        tree.children[transaction[0]].count += count
    else:
        new_node = TreeNode(transaction[0], count, tree)
        tree.children[transaction[0]] = new_node
        if header_table[transaction[0]][1] is None:
            header_table[transaction[0]][1] = new_node
        else:
            node = header_table[transaction[0]][1]
            while node.link is not None:
                node = node.link
            node.link = new_node

    if len(transaction) > 1:
        add_transaction(tree.children[transaction[0]], transaction[1:], header_table, count)


# Konstrukcija FP-drveta
def construct_fp_tree(transactions):
    
    header_table = {}
    
    for transaction in transactions:
        for item in transaction:
            header_table[item] = header_table.get(item, 0) + 1
    
    header_table = {item: [support, None] for item, support in header_table.items()}
    
    if len(header_table) == 0:
        return None, None

    tree = TreeNode('Null', None, None)
    
    for transaction in transactions:
        transaction = [item for item in transaction if item in header_table] 
        transaction = sorted(transaction, key=lambda item: (-header_table[item][0], item))
        transaction = list(dict.fromkeys(transaction))
        
        if len(transaction) > 0:
            add_transaction(tree, transaction, header_table, 1)

    return tree, header_table


# Vizualizacija FP-drveća
def visualize_tree(tree, fig, ax):
    
    G = nx.DiGraph()
    pos = {}
    levels = defaultdict(list)
    node_queue = [(tree, str(id(tree)), 0)]
    
    while node_queue:
        node, node_id, level = node_queue.pop(0)
        G.add_node(node_id, label=node.name, count=node.count)
        levels[level].append(node_id)
        
        for child in node.children.values():
            child_id = str(id(child))
            G.add_edge(node_id, child_id)
            node_queue.append((child, child_id, level + 1))

    for level, nodes in levels.items():
        num_nodes = len(nodes)
        for i, node in enumerate(nodes):
            pos[node] = (i - num_nodes / 2, -level) 

    labels = {node: '\n\nNull' if data['label'] == 'Null' else '\n\n{} : {}'.format(data['label'], data['count']) for node, data in G.nodes(data=True)}
    ax.clear()
    nx.draw(G, pos, labels=labels, with_labels=True, ax=ax)


# Crtanje FP-drveta
def draw_fp_tree(transactions_text, min_support_entry, fp_tree_canvas):

    if not validate_input(transactions_text, min_support_entry, False):
        return

    transactions = [line.split() for line in transactions_text.get('1.0', 'end').split('\n') if line]

    # Generisanje FP-drveta
    global fig
    fig = plt.figure(figsize=(6, 4)) 
    ax = fig.add_subplot(111)
    tree, header_table = construct_fp_tree(transactions)

    # Vizuelizacija FP-drveta
    visualize_tree(tree, fig, ax)

    # Uklanjanje prethodno dodatih widgete-a
    for widget in fp_tree_canvas.winfo_children():
        widget.destroy()  
    
    # Prikazivanje figure na canvasu
    canvas = FigureCanvasTkAgg(fig, master=fp_tree_canvas)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Funkcija za čuvanje slike
def save_image():

    global fig

    if fig is None:  # Provera da li postoji figura
        tk.messagebox.showerror("Greška", "Nema figure za čuvanje.")
        return
    
    # Otvaranje dijaloga za čuvanje fajla
    file_path = tk.filedialog.asksaveasfilename(defaultextension=".png")

    # Provera da li je korisnik uneo putanju do fajla
    if file_path:
        if fig is not None:  
            fig.savefig(file_path) 
        else:
            print("Nema figure za čuvanje.")


# Funkcija za pronalaženje čestih skupova stavki
def find_frequent_itemsets(transactions_text, min_support_entry, frequent_itemsets_text):
    
    # Provera validnosti unosa
    if not validate_input(transactions_text, min_support_entry):
        return

    # Izvlačenje transakcija i minimalne podrške iz unosa
    transactions = transactions_text.get('1.0', 'end-1c').split('\n')
    transactions = [list(set(transaction.split())) for transaction in transactions]  # Pretvaranje transakcija u skupove
    min_support = int(min_support_entry.get())

    # Pronalaženje čestih skupova stavki
    patterns = pyfpgrowth.find_frequent_patterns(transactions, min_support)

    # Ispisivanje čestih skupova stavki
    frequent_itemsets_text.config(state='normal')
    frequent_itemsets_text.delete('1.0', 'end')
    for itemset, support in patterns.items():
        if len(itemset) > 1:  
            frequent_itemsets_text.insert('end', f"{' '.join(itemset)}: {support}\n")
    frequent_itemsets_text.config(state='disabled')


# Funkcija za čuvanje čestih skupova stavki
def save_frequent_itemsets(frequent_itemsets_text):

    content = frequent_itemsets_text.get('1.0', 'end-1c')
    if not content.strip():  # Provera da li postoji tekst
        tk.messagebox.showerror("Greška", "Nema teksta za čuvanje.")
        return
    
    # Otvaranje dijaloga za čuvanje datoteke
    filepath = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not filepath:  # Ako korisnik otkaže operaciju čuvanja
        return
    
    with open(filepath, 'w') as file:
        # Čitanje sadržaja i čuvanje u datoteku
        content = frequent_itemsets_text.get('1.0', 'end-1c')
        file.write(content)


# Funkcija za rukovanje greškama
def validate_input(transactions_text, min_support_entry, check_min_support=True):
    
    # Izvlačenje transakcija iz unosa
    transactions = transactions_text.get('1.0', 'end-1c').split('\n')

    # Provera da li su unete transakcije
    if not transactions or all(not transaction for transaction in transactions):
        tk.messagebox.showerror("Greška", "Morate uneti transakcije.")
        return False

    # Ako je potrebno, provera da li je uneta minimalna podrška
    if check_min_support:
        min_support = min_support_entry.get()
        if not min_support:
            tk.messagebox.showerror("Greška", "Morate uneti minimalnu podršku.")
            return False

        # Provera da li je minimalna podrška pozitivan ceo broj
        try:
            min_support = int(min_support)
            if min_support <= 0:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror("Greška", "Minimalna podrška mora biti pozitivan ceo broj.")
            return False

    return True


def create_gui():
    
    # Kreiranje glavnog prozora
    window = tk.Tk()
    window.title("FP-Tree Constructor")

    # Konfiguracija redova i kolona za skaliranje
    for i in range(7): 
        window.grid_rowconfigure(i, weight=1)
    for i in range(3):
        window.grid_columnconfigure(i, weight=1)

    # Postavljanje funkcije koja se poziva kada se prozor zatvori
    window.protocol("WM_DELETE_WINDOW", window.quit)

    # Dugme za učitavanje transakcija
    load_button = tk.Button(window, text="Učitaj transakcije", command=lambda: load_transactions(transactions_text))
    load_button.grid(row=0, column=0, sticky='nsew', pady=(10, 5), columnspan=4)

    # Polje za unos transakcija
    tk.Label(window, text="Unesite transakcije (svaka transakcija u novom redu):").grid(row=1, column=0, sticky='w', columnspan=3)
    transactions_text = tk.Text(window, height=10)
    transactions_text.grid(row=2, column=0, sticky='nsew', columnspan=3)
    transactions_scrollbar = tk.Scrollbar(window, command=transactions_text.yview)
    transactions_scrollbar.grid(row=2, column=3, sticky='ns')
    transactions_text['yscrollcommand'] = transactions_scrollbar.set

    # Polje za unos minimalne podrške
    tk.Label(window, text="Unesite minimalnu podršku:").grid(row=3, column=0, sticky='nsew', columnspan=4)
    min_support_entry = tk.Entry(window)
    min_support_entry.grid(row=4, column=0, sticky='nsew', columnspan=4, pady=(0, 10))

    # Canvas za crtanje FP-drveta
    fp_tree_canvas = tk.Canvas(window)
    draw_button = tk.Button(window, text="Nacrtaj FP-drvo", command=lambda: draw_fp_tree(transactions_text, min_support_entry, fp_tree_canvas))
    draw_button.grid(row=5, column=0, sticky='nsew', pady=(0, 10), columnspan=2)
    
    tk.Label(window, text="FP-drvo:").grid(row=6, column=0, sticky='w', columnspan=2)
    fp_tree_canvas.grid(row=7, column=0, columnspan=2)

    # Dugme za pronalaženje čestih skupova stavki
    find_frequent_itemsets_button = tk.Button(window, text="Odredi česte skupove stavki", command=lambda: find_frequent_itemsets(transactions_text, min_support_entry, frequent_itemsets_text))
    find_frequent_itemsets_button.grid(row=5, column=2, sticky='nsew', pady=(0, 10), columnspan=2)

    # Polje za prikaz čestih skupova stavki
    tk.Label(window, text="Česti skupovi stavki:").grid(row=6, column=2, sticky='w', columnspan=2)
    frequent_itemsets_text = tk.Text(window, height=10, state='disabled')
    frequent_itemsets_text.grid(row=7, column=2, sticky='nsew')
    frequent_itemsets_scrollbar = tk.Scrollbar(window, command=frequent_itemsets_text.yview)
    frequent_itemsets_scrollbar.grid(row=7, column=3, sticky='ns')
    frequent_itemsets_text['yscrollcommand'] = frequent_itemsets_scrollbar.set

    # Dugme za čuvanje slike
    save_image_button = tk.Button(window, text="Sačuvaj sliku", command=save_image)
    save_image_button.grid(row=8, column=0, columnspan=2, sticky='nsew', pady=(20, 10))

    # Dugme za čuvanje čestih skupova stavki u .txt datoteku
    save_frequent_itemsets_button = tk.Button(window, text="Sačuvaj česte skupove stavki", command=lambda: save_frequent_itemsets(frequent_itemsets_text))
    save_frequent_itemsets_button.grid(row=8, column=2, columnspan=2, sticky='nsew', pady=(20, 10))

    # Pokretanje glavne petlje za prozor
    window.mainloop()


if __name__ == "__main__":
    create_gui()