import csv
import os 
from datetime import datetime
csv_f = "manager.csv" 
header = ['Date','Category','Amount']
def my_csv():
    if not os.path.isfile(csv_f):
        with open(csv_f, "w", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)             
def read_exp(): 
    my_csv()
    with open(csv_f, "r", newline="", encoding='utf-8') as f:
        read = csv.DictReader(f)
        return list(read)
def writ_exp(rows): 
    with open(csv_f, "w", newline="", encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
def add_exp():
    d = input("Enter the date in YYYY-MM-DD using '-' to separate date month and year(Leave blank for today's date) : ").strip() 
    if not d :
        d = datetime.today().strftime('%Y-%m-%d')
    try:
        datetime.fromisoformat(d)
    except Exception:
        print("Invalid Format Please convert it to YYYY-MM-DD")
        return
    c = input("Category of the purchase (Leave blank for Miscellaneous Purchase): ").strip() or "Misc"
    amt = input("Enter the amount of purchase : ").strip()
    try:
        amt_ = float(amt)
    except ValueError:
        print("Invalid format for amount, Use Numbers ")
        return
    my_csv()
    with open(csv_f, "a", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([d, c, f'{amt_:.2f}'])
    print("Expense added")    
def view_exp():
    rows = read_exp()
    if not rows :
        print("No Expense added")
        return
    print("Index  Date  Category  Amount")
    print("_"*45)
    t = 0.0
    i=1
    for r in rows:
        amt_ = float(r['Amount'])
        t+=amt_
        print(f'{i:<6}   {r['Date']}   {r['Category']}   {r['Amount']} ')
        i+=1
    print("_"*45)
    print(f"Total Amount Spend {t:.2f}")
def del_exp():
    rows = read_exp()
    view_exp()
    if not rows :
        print("Nothing to delete") 
        return
    ind= input("Enter the Index No. to delete (Leave blank to cancel) : ").strip()    
    if not ind :
        print("Operation Cancelled ")
        return
    try:
        i=int(ind)
        if i < 1 or i > len(rows):
            print("Invalid Index No.")
            return
    except ValueError:
        print("Enter a valid Number, Index can't be in words you know (>_<)")
        return
    del rows[i-1]
    writ_exp(rows)
    print("Entry Deleted")
def sum_total():
    rows = read_exp()
    if not rows : 
        print("No Registered data")
        return
    t=0.0
    c_sum = {}
    for r in rows:
        amt_=float(r['Amount'])
        t+=amt_
        c=r['Category']
        c_sum[c] = c_sum.get(c,0.0)+amt_
    print(f"Total spent Amount {t:.2f}")
    print("By Category : ")
    for a,b in c_sum.items():
        print(f"- {a}: {b:.2f}")
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None
def menu():
    my_csv()
    while True:
        print(" == Personal Budget and Expense Tracker == ")
        print("1. Add Expense\n2. View Expenses\n3. Delete Expenses\n4. Summary of the total spend\n5. Exit")
        ch = input("Enter your Choice :  ").strip()
        if ch == "1":
            add_exp()
        elif ch == "2":
            view_exp()
        elif ch == "3":
            del_exp()
        elif ch == "4":
            sum_total()
        elif ch == "5": 
            print("BY!!! BY!!!")
            break
        else:
            print("The choice is Invalid")
menu()
       
