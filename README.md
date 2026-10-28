# Expense Tracker

A desktop expense tracker built with Python and Tkinter. Add your expenses, see them in a table, delete the ones you don't need, and view your spending by category with bar and pie charts. Your data is saved automatically, so it's still there when you reopen the app.
<h2>Home page</h2><br>
<img width="640" height="582" alt="Screenshot 2026-10-28 205159" src="https://github.com/user-attachments/assets/490ecdeb-29df-4b80-9880-c6fbfed2cf55" /><br>
<h2>Main page</h2><br>
<img width="845" height="692" alt="Screenshot 2026-10-28 205207" src="https://github.com/user-attachments/assets/e7cea699-de4a-4077-ad8b-715dbda9f7c1" /><br>
<h2>Charts page</h2><br>
<img width="1107" height="882" alt="Screenshot 2026-10-28 205222" src="https://github.com/user-attachments/assets/f2d0ff4e-620a-4346-8258-b6317ab2ca01" /><br>


## Features

- Add an expense with a name, category, amount, and date
- Input checks: the name can't be empty, and the amount must be a positive number
- All expenses shown in a table (`ttk.Treeview`)
- Delete one or more selected expenses (the S.no column renumbers itself)
- Data saved to a JSON file and loaded again at startup
- Totals page with:
  - the amount spent in each category
  - a bar chart of spending by category
  - a pie chart of the spending distribution
- Three pages: Home, Expenses, and Totals

## Tech stack

- Python 3
- Tkinter and `ttk` (included with Python)
- `json` (included with Python)
- [Matplotlib](https://matplotlib.org/) for the charts

## Installation and setup

1. Make sure Python 3 is installed:
   ```bash
   python --version
   ```
2. Clone this repository:
   ```bash
   git https://github.com/TvSivajaswanth/Expense-tracker-using-Python.git
   ```
3. Install the one required package:
   ```bash
   pip install matplotlib
   ```
4. Run the app:
   ```bash
   python main.py
   ```

If you see `ModuleNotFoundError: No module named 'matplotlib'`, step 3 didn't finish. Run it again.

## How to use

1. Click **Click to Track** on the home page.
2. Fill in the name, choose a category, enter the amount, and type a date (for example `27 Oct`).
3. Click **Add**. The expense appears in the table and is saved right away.
4. To remove an expense, select its row and click **Delete**. Hold Ctrl to select several rows.
5. Click **Total Expense** to see the totals and charts.

## Categories

Food, Travel, Bills, Shopping, and Other.

## Project structure

```
expense-tracker/
├── main.py            # the whole application
├── store_data.json    # created automatically after you add an expense
└── README.md
```

## How the data is stored

Every expense is a dictionary in a list, saved in `store_data.json`:

```json
[
    {
        "id": 1,
        "name": "Lunch",
        "category": "Food",
        "amount": 150.0,
        "date": "27 Oct"
    }
]
```

If the file doesn't exist yet, the app starts with an empty list. If the file is damaged, the app shows a warning and starts empty.

## How it works

- **Pages:** each page is a `Frame` stacked in the same grid cell. `show_page()` brings one to the front with `tkraise()`.
- **Table and data stay in sync:** the Treeview is only a display, and the real data is the `data` list. Adding or deleting changes the list, then the file is saved.
- **Totals:** the app loops through the expenses and adds each amount to its category in a dictionary.
- **Charts:** Matplotlib figures are drawn inside Tkinter with `FigureCanvasTkAgg`. The old chart is destroyed before a new one is drawn, so charts don't pile up on the page.

## What I learned

- Building multi-page Tkinter apps
- Using `ttk.Treeview` and `ttk.Combobox`
- Reading and writing JSON, including handling a missing or damaged file
- Validating user input with `try` / `except`
- Keeping a display (the table) and the real data (the list) in sync
- Embedding Matplotlib charts in a Tkinter window

## A note on how this was built

I wrote the main app myself while learning, including the form, the table, saving and loading, and the delete and totals logic. The Matplotlib chart code was written with AI assistance, and I'm studying it so I can explain how it works.

## Known limitations and future improvements

- [ ] Prefill the date box with today's date
- [ ] Keep the category list in one place so adding a category is a single change
- [ ] Show an overall total spent
- [ ] Filter the totals by month
- [ ] Edit an existing expense
- [ ] Search or filter the table by category
- [ ] Export expenses to CSV

## License

This project is open source and free to use for learning.
