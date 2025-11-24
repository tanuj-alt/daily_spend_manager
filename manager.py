import csv
import os 
from datetime import datetime
csv_f = "manager.csv" 
header = ['Date','Category','Amount']
def my_csv():                                                # This function is there to create a csv file if it's not already there
    if not os.path.isfile(csv_f):
        with open(csv_f, "w", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)             
def read_exp():                                               # This function is used later in the program to read the data entered in csv file
    my_csv()
    with open(csv_f, "r", newline="", encoding='utf-8') as f:
        read = csv.DictReader(f)
        return list(read)
def writ_exp(rows):                                           # This Function is used to write the entries in csv file created
    with open(csv_f, "w", newline="", encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
def add_exp():                                                 # To create Entries of expenses made
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
def view_exp():                                                     # To view the entries that are created
    rows = read_exp()
    if not rows :
        print("No Expense added yet")
        return
    print("Index   Date   Category   Amount ")
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
def del_exp():                                                      #To delete the entries of expenses that are created 
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
def plot_cat():                                         # Basic Graph of Summary of all the expenses made
    if plt is None:
        print("Matplotlib is not installed, Run 'pip install matplotlib' to install it ")
        return
    rows = read_exp()
    if not rows : 
        print("No Registered data")
        return
    c_sum={}
    for r in rows:
        amt_=float(r['Amount'])
        c=r['Category']
        c_sum[c] = c_sum.get(c,0.0)+amt_
    cat=list(c_sum.keys())
    amt=[c_sum[c] for c in cat]
    plt.bar(cat,amt)
    plt.title("Spending by category : ")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.show()
def plot_date():                                         #Graph of a basic summary of Monthly Expenses
    if plt is None:
        print("Matplotlib is not installed, Run 'pip install matplotlib' to install it ")
        return
    rows = read_exp()
    if not rows : 
        print("No Registered data")
        return
    mon_sum={}
    for r in rows :
        d=r['Date']
        try :
            dat = datetime.fromisoformat(d)
        except Exception:
            continue
        k=f"{dat.year}-{dat.month:02d}"
        amt=float(r['Amount'])
        mon_sum[k]=mon_sum.get(k,0.0) + amt 
    key=sorted(mon_sum.keys())
    val=[mon_sum[k] for k in key]
    plt.plot(key, val)
    plt.title("Monthly Expenses :")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.show()
def menu():                                                #Console to take all the user input and Perform tasks accordingly
    my_csv()
    while True:
        print("          == Personal Budget and Expense Tracker ==       ")
        print("1. Add Expense\n2. View Expenses\n3. Delete Expenses\n4. Summary of the total spend\n5. Plot by Category\n6. Plot by Monthly spending\n7. Exit")
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
            plot_cat()
        elif ch == "6":
            plot_date()
        elif ch == "7":
            print("Peace Out!!")
            break
        else:
            print("Invalid Choice")
menu()
       
