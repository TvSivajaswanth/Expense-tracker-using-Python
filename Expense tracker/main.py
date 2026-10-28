from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
root = Tk()
root.geometry("900x900")
box = Frame(boxparent := root)
box.pack(fill="both", expand=True)

def load_info():
    try:
        with open("store_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []                      # first run: no expenses yet
    except json.JSONDecodeError:
        messagebox.showwarning("Error", "store_data.json is damaged, starting empty.")
        return []
    
def save_info():
    with open("store_data.json", "w") as file:
          json.dump(data, file, indent=4)
home_page = Frame(box)
main_page = Frame(box)
track_expense = Frame(box)


pages = [
     home_page,main_page,track_expense   
]

for page in pages:
    page.grid(row=0,column=0, sticky="nsew")



def show_page(page):
    page.tkraise()
    
data = load_info()


Label(
    home_page,
    text="Expense tracker",
    font=("Arial", 20, "bold")
).pack(pady=10,padx=10)
              
Button(home_page,text="Click to Track",font=("Arial",18,"bold"),width=20,command=lambda:show_page(main_page)).pack(padx=10,pady=10)         
Button(home_page,text="Exit",font=("Arial",18,"bold"),width=20,command=root.quit).pack(padx=10,pady=10)         
# ============form page====================
form_frame = Frame(main_page)
form_frame.pack()
Label(form_frame,text="Nmae").grid(row=0,column=0,sticky="w",padx=5)
Label(form_frame,text="Category").grid(row=0,column=1,sticky="w",padx=5)
Label(form_frame,text="Amount").grid(row=0,column=2,sticky="w",padx=5)
Label(form_frame,text="Date").grid(row=0,column=3,sticky="w",padx=5)

name_entry = Entry(form_frame, width=25)
name_entry.grid(row=1, column=0, padx=5)


category_box  = ttk.Combobox(
    form_frame,
    values=["Food", "Travel", "Bills", "Shopping", "Other"],
    state="readonly",
    width=15
)
category_box.current(0)
category_box.grid(row=1, column=1, padx=5)

amount_entry = Entry(form_frame, width=12)
amount_entry.grid(row=1, column=2, padx=5)

date_entry = Entry(form_frame, width=12)
date_entry.grid(row=1, column=3, padx=5)



tree = ttk.Treeview(main_page,columns=("S.no","name","category","amount","date"),show="headings")
tree.heading("S.no", text="S.no")
tree.heading("name", text="Name")
tree.heading("category", text="Category")
tree.heading("amount", text="Amount")
tree.heading("date", text="Date")

tree.column("S.no",width=40, anchor="e")
tree.column("name", width=150, anchor="e")
tree.column("category", width=100, anchor="e")
tree.column("amount", width=80, anchor="e")
tree.column("date", width=80, anchor="e")

tree.pack(anchor = "center")

def add_info():
    
    try:
        amount = float(amount_entry.get())
        
        if amount <= 0:
            messagebox.showwarning("Invalid amount", "Amount Not be a Negitive number.")
            return
    except ValueError:
        messagebox.showwarning("Invalid amount", "Amount must be a number.")
        return
    id = max(
        (item["id"] for item in data),
        default=0
        ) + 1
    name = name_entry.get()
   
    if not name:
        messagebox.showwarning("Invalid amount", "Enter a name is empty")
        return   
    
    new_task = {
        "id": id,
        "name": name,
        "category": category_box.get(),
        "amount":amount,
        "date":date_entry.get()
    }
    
    tree.insert("", 
                END, 
                values=(
                    id, 
                    new_task["name"], 
                    new_task["category"], 
                    new_task["amount"], 
                    new_task["date"]
                ))
    
    data.append(new_task)
    save_info()
    name_entry.delete(0, END)
    amount_entry.delete(0, END)
    date_entry.delete(0, END)
def show_all():
    for e in data:
        tree.insert("", 
                        END, 
                        values=(
                            e["id"], 
                            e["name"], 
                            e["category"], 
                            e["amount"], 
                            e["date"]
                        ))
show_all()
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    for e in data:
        tree.insert("", END, values=(e["id"], e["name"], e["category"], e["amount"], e["date"]))
def delete_info():
    
    selected = tree.selection()
    
    if not selected:
        messagebox.showwarning("Nothing selected", "Select a row first.")
        return
    
    for row_id in selected:
            value = tree.item(row_id,"values")
            id = int(value[0])
            for expense in data:
                if expense["id"] == id:
                    data.remove(expense)
                    break
            tree.delete(row_id)       
            
    for number, expense in enumerate(data,start=1):
        expense["id"] = number
    refresh_table()                   
    save_info()  

Button(form_frame, text="Add", width=10,command=add_info).grid(row=1, column=4,pady=10,padx=5)
Button(main_page,text="datete",width=20,height=2,command=delete_info).pack(padx=10,pady=10)

# Create these labels once, before defining total()

food_label = Label(track_expense, font=("Arial", 10, "bold"))
food_label.pack(pady=10, padx=10)

travel_label = Label(track_expense, font=("Arial", 10, "bold"))
travel_label.pack(pady=10, padx=10)

bills_label = Label(track_expense, font=("Arial", 10, "bold"))
bills_label.pack(pady=10, padx=10)

shopping_label = Label(track_expense, font=("Arial", 10, "bold"))
shopping_label.pack(pady=10, padx=10)

other_label = Label(track_expense, font=("Arial", 10, "bold"))
other_label.pack(pady=10, padx=10)


def total():
    totals = {
        "Food": 0.0,
        "Travel": 0.0,
        "Bills": 0.0,
        "Shopping": 0.0,
        "Other": 0.0
    }

    for e in data:
        category = e["category"]
        if category in totals:
            totals[category] += float(e["amount"])

    food_label.config(
        text=f"Expense on Food: {totals['Food']:.2f} /Month"
    )
    travel_label.config(
        text=f"Expense on Travel: {totals['Travel']:.2f} /Month"
    )
    bills_label.config(
        text=f"Expense on Bills: {totals['Bills']:.2f} /Month"
    )
    shopping_label.config(
        text=f"Expense on Shopping: {totals['Shopping']:.2f} /Month"
    )
    other_label.config(
        text=f"Expense on Other: {totals['Other']:.2f} /Month"
    )
    
chart_frame = Frame(track_expense)
chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

chart_canvas = None

def show_charts():
    global chart_canvas

    categories = ["Food", "Travel", "Bills", "Shopping", "Other"]
    totals = {category: 0.0 for category in categories}

    
    for expense in data:
        category = expense["category"]
        if category in totals:
            totals[category] += float(expense["amount"])

    values = [totals[category] for category in categories]

   
    fig = Figure(figsize=(9, 4), dpi=100)

    bar_ax = fig.add_subplot(121)
    pie_ax = fig.add_subplot(122)

    
    bar_ax.bar(categories, values)
    bar_ax.set_title("Expenses by Category")
    bar_ax.set_ylabel("Amount")
    bar_ax.tick_params(axis="x", rotation=35)

   
    if sum(values) > 0:
        pie_ax.pie(
            values,
            labels=categories,
            autopct="%1.1f%%",
            startangle=90
        )
        pie_ax.set_title("Spending Distribution")
    else:
        pie_ax.text(
            0.5, 0.5,
            "No expenses yet",
            ha="center",
            va="center"
        )
        pie_ax.set_title("Spending Distribution")
        pie_ax.axis("off")

    fig.tight_layout()

   
    if chart_canvas is not None:
        chart_canvas.get_tk_widget().destroy()

    chart_canvas = FigureCanvasTkAgg(
        fig,
        master=chart_frame
    )
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )
   
total()
show_charts()
def refresh_total():
    total()
    show_charts()
    
Button(
    main_page,
    text="Total Expense",
    width=20,
    height=2,
    command=lambda: (
        refresh_total(),
        show_charts(),
        show_page(track_expense)
    )
).pack(padx=10, pady=10)

Button(main_page, text="Go to home page", width=20,height=2,command=lambda:show_page(home_page)).pack(padx=5,pady=5)
Button(track_expense, text="Go to home page", width=20,height=2,command=lambda:show_page(home_page)).pack(padx=5,pady=5)               
show_page(home_page)
root.mainloop()