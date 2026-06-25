import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import datetime
import requests

import webbrowser

URL = "https://primer1.soton.ac.uk/cgi-bin/runprimer1.cgi"

def open_url(url):
    webbrowser.open(url)


def clean(seq):
    return seq.replace("\n", "").replace(" ", "").strip()


# ================= SAVE =================
def save_to_txt():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )

    if not file_path:
        return

    seq = clean(text_seq.get("1.0", tk.END))
    result = output.get("1.0", tk.END)

    content = f"""Primer1 Results
====================
Date: {datetime.datetime.now()}

DNA Sequence:
{seq}

====================
RESULTS:
{result}
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    messagebox.showinfo("Saved", "File saved successfully")


# ================= RUN =================
def run_primer():
    seq = clean(text_seq.get("1.0", tk.END))

    if not seq:
        messagebox.showerror("Error", "Please enter DNA sequence")
        return

    params = [
        seq,
        e_snp_pos.get(),
        e_allele1.get(),
        e_allele2.get(),
        e_opt_size.get(),
        e_max_size.get(),
        e_min_size.get(),
        e_opt_product.get(),
        e_max_product.get(),
        e_min_product.get(),
        e_max_ratio.get(),
        e_min_ratio.get(),
        e_opt_tm.get(),
        e_max_tm.get(),
        e_min_tm.get(),
        e_max_gc.get(),
        e_min_gc.get(),
        e_max_compl.get(),
        e_max_3compl.get(),
        e_salt.get(),
        e_primer_conc.get(),
        e_outputs.get()
    ]

    inputs = "+".join(params)

    try:
        r = requests.get(URL + "?" + inputs, timeout=30)
        output.delete("1.0", tk.END)
        output.insert(tk.END, r.text)
    except Exception as e:
        messagebox.showerror("Request Error", str(e))


# ================= UI =================
root = tk.Tk()
root.title("Primer1 GUI - Primer design for: Tetra Arms PCR (Network connection required. Server source: https://primer1.soton.ac.uk/primer1.html)")
root.geometry("1000x900+20+20")


# ================= DNA INPUT =================
dna_frame = tk.LabelFrame(root, text="Enter DNA sequence (up to 1,000 bases. target SNP can be marked by square brackets.)", padx=5, pady=5)
dna_frame.pack(fill="x", padx=5, pady=5)

text_seq = scrolledtext.ScrolledText(dna_frame, height=5)
text_seq.pack(fill="x")


# ================= PARAMETERS =================
params_frame = tk.LabelFrame(root, text="PCR Parameters", padx=5, pady=5)
params_frame.pack(fill="x", padx=5, pady=5)


# ---- Sub Frames ----
general_frame = tk.LabelFrame(params_frame, text="General (change values)")
general_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

size_frame = tk.LabelFrame(params_frame, text="Primer length")
size_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

product_frame = tk.LabelFrame(params_frame, text="Inner Products lengthes")
product_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

tm_frame = tk.LabelFrame(params_frame, text="Tm / GC")
tm_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

complex_frame = tk.LabelFrame(params_frame, text="Chance for complementarity and dimer")
complex_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

chem_frame = tk.LabelFrame(params_frame, text="Chemistry")
chem_frame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)


def add(parent, label, default):
    f = tk.Frame(parent)
    f.pack(fill="x", pady=2)

    tk.Label(f, text=label, width=22, anchor="w").pack(side="left")
    e = tk.Entry(f, width=10)
    e.insert(0, default)
    e.pack(side="right")
    return e


# ================= GENERAL =================
e_snp_pos = add(general_frame, "SNP position (in sequence)", "501")
e_allele1 = add(general_frame, "Allele 1 (As in sequence)", "X")
e_allele2 = add(general_frame, "Allele 2 (Derived allele)", "Y")
e_outputs = add(general_frame, "Num. of Outputs requested", "10")

# ================= SIZE =================
e_opt_size = add(size_frame, "Opt primer length", "28")
e_max_size = add(size_frame, "Max length", "30")
e_min_size = add(size_frame, "Min length", "26")

# ================= PRODUCT =================
e_opt_product = add(product_frame, "Opt length", "200")
e_max_product = add(product_frame, "Max length", "300")
e_min_product = add(product_frame, "Min length", "100")
e_max_ratio = add(product_frame, "Max 2 amplicons diff (was 1.5)", "2")
e_min_ratio = add(product_frame, "Min 2 amplicons diff (was 1.1)", "1.5")

# ================= TM / GC =================
e_opt_tm = add(tm_frame, "Opt Tm", "65")
e_max_tm = add(tm_frame, "Max Tm", "80")
e_min_tm = add(tm_frame, "Min Tm", "50")
e_max_gc = add(tm_frame, "Max GC", "80")
e_min_gc = add(tm_frame, "Min GC", "20")

# ================= COMPLEXITY =================
e_max_compl = add(complex_frame, "Max complementarity", "8")
e_max_3compl = add(complex_frame, "3' complementarity (Dimer)", "3")

# ================= CHEMISTRY =================
e_salt = add(chem_frame, "Salt concentration (mM)", "50")
e_primer_conc = add(chem_frame, "primer concentration (nM)", "50")



# make grid expand nicely
for i in range(3):
    params_frame.columnconfigure(i, weight=1)
for i in range(2):
    params_frame.rowconfigure(i, weight=1)


# ================= BUTTONS =================
btn_frame = tk.Frame(root)
btn_frame.pack(fill="x", pady=5)

tk.Button(btn_frame, text="Find Primers", command=run_primer, bg="lightblue").pack(side="left", padx=10)
tk.Button(btn_frame, text="Save Output to TXT", command=save_to_txt, bg="lightgreen").pack(side="left", padx=10)
tk.Button(btn_frame, text="Open Primer1 Website", command=lambda: open_url("https://primer1.soton.ac.uk/primer1.html"), bg="mistyrose").pack(side="left", padx=10)
tk.Button(btn_frame, text="Open Help Page", command=lambda: open_url("https://primer1.soton.ac.uk/primer1help.html"), bg="mistyrose").pack(side="left", padx=10)

# ================= OUTPUT =================
out_frame = tk.LabelFrame(root, text="Output", padx=5, pady=5)
out_frame.pack(fill="both", expand=True, padx=5, pady=5)

output = scrolledtext.ScrolledText(out_frame)
output.pack(fill="both", expand=True)


root.mainloop()


