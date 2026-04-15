import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import csv
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

root = tk.Tk()
root.title("Cancer Detection Portal")
root.geometry("600x650")
root.configure(bg="#f4f7f6")

header = tk.Frame(root, bg="#2c3e50", height=80)
header.pack(fill="x")
tk.Label(header, text="Cancer Detection Portal", font=("Segoe UI", 20, "bold"), fg="white", bg="#2c3e50", pady=20).pack()
def view_history():
    history_win = tk.Toplevel(root)
    history_win.title("Prediction History")
    history_win.geometry("700x400")
    
    cols = ("Radius", "Texture", "Area", "Smoothness", "Result", "Timestamp")
    tree = ttk.Treeview(history_win, columns=cols, show="headings")
    
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    try:
        with open("history.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", "end", values=row)
    except FileNotFoundError:
        messagebox.showinfo("Info", "No history found yet.")
    
    tree.pack(fill="both", expand=True, padx=10, pady=10)

def predict():
    try:
        r, t, a, s = float(e1.get()), float(e2.get()), float(e3.get()), float(e4.get())
        data_scaled = scaler.transform([[r, t, a, s]])
        res = model.predict(data_scaled)[0]

        if res == 1:
            msg = "Malignant - Cancer detected, please consult a doctor"
            color, bg_color = "#922b21", "#f9ebea"
            res_text = "Malignant"
        else:
            msg = "Benign - Non-cancerous, but medical consultation advised"
            color, bg_color = "#1d8348", "#e9f7ef"
            res_text = "Benign"

        output_label.config(text=msg, fg=color, bg=bg_color)
        
        with open("history.csv", "a", newline="") as f:
            csv.writer(f).writerow([r, t, a, s, res_text, datetime.now().strftime("%Y-%m-%d %H:%M")])
            
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values")

main_frame = tk.Frame(root, bg="#f4f7f6", pady=20)
main_frame.pack()

def create_entry(label_text):
    tk.Label(main_frame, text=label_text, font=("Segoe UI", 10), bg="#f4f7f6").pack(pady=(10, 0))
    entry = tk.Entry(main_frame, font=("Segoe UI", 12), bd=1, width=30)
    entry.pack(pady=5)
    return entry

e1 = create_entry("Radius Mean")
e2 = create_entry("Texture Mean")
e3 = create_entry("Area Mean")
e4 = create_entry("Smoothness Mean")

tk.Button(main_frame, text="Predict Now", command=predict, bg="#27ae60", fg="white", font=("Segoe UI", 12, "bold"), width=20, bd=0, cursor="hand2").pack(pady=20)
tk.Button(main_frame, text="View History", command=view_history, bg="#2980b9", fg="white", font=("Segoe UI", 10), width=15, bd=0, cursor="hand2").pack()

output_label = tk.Label(root, text="Result will appear here", font=("Segoe UI", 11, "bold"), width=50, height=4, bg="#ebedef", relief="flat", wraplength=400)
output_label.pack(pady=30)

root.mainloop()