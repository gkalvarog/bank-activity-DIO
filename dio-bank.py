import datetime, pytz

bank_log = []
clients = []
current_customer = None
LIMIT_DAILY_TRANSACTIONS = 10

menu = """
Menu
[d] Deposit
[w] Withdraw
[s] Statement
[n] New account
[l] Login
[o] Logout
[e] Exit
=> """

class Client:
    def __init__(self, name, taxid):
        self.name = name
        self.taxid = taxid
        self.transactions = [] 
        self.balance = 0
        self.transactions_made = 0

    def make_transaction(self, transaction):
        if self.transactions_made >= LIMIT_DAILY_TRANSACTIONS:
            print("You have exceeded the number of transactions allowed for today!")
            return False
        self.transactions.append(transaction)
        self.transactions_made += 1
        return True

    def deposit(self, amt):
        now = datetime.datetime.now(pytz.utc).strftime("%Y-%m-%d, %H:%M:%S, UTC")
        if self.make_transaction(Transaction("d", amt, now)):
            self.balance += amt
            bank_log.append(f"Deposit: {amt} on {now}, New Balance: {self.balance}")
            print(f"Deposit successful. New Balance: ${self.balance}")
        else:
            print("Transaction failed.")

    def withdraw(self, amt):
        now = datetime.datetime.now(pytz.utc).strftime("%Y-%m-%d, %H:%M:%S, UTC")
        if self.balance >= amt:
            if self.make_transaction(Transaction("w", amt, now)):
                self.balance -= amt
                bank_log.append(f"Withdrawal: {amt} on {now}, New Balance: {self.balance}")
                print(f"Withdrawal successful. New Balance: ${self.balance}")
            else:
                print("Transaction failed.")
        else:
            print(f"Insufficient funds. You can withdraw up to ${self.balance}.")

    def show_statement(self):
        print(f"Balance: ${self.balance}")
        if self.transactions:
            print("Transaction History:")
            for transaction in self.transactions:
                print(f"Type: {transaction.type}, Amount: ${transaction.amount}, Date: {transaction.date}")
        else:
            print("No transactions to show.")

class Transaction:
    def __init__(self, type, amount, date):
        self.type = type
        self.amount = amount
        self.date = date

def create_new_account(name, taxid):
    clients.append(Client(name, taxid))
    now = datetime.datetime.now(pytz.utc).strftime("%Y-%m-%d, %H:%M:%S, UTC")
    bank_log.append(f"Account Creation: Name: {name}, Tax ID: {taxid}, Time: {now}")
    print(f"Account created successfully.")

def set_current_user(taxid):
    result = list(filter(lambda p: p.taxid == taxid, clients))
    if result:
        return result[0]
    else:
        print("Account not found.")
        return None

def want_to_continue():
    return input("Would you like to make another operation? (y/n)\n").lower() == "y"

def print_final_log():
    print("\n--- Session Log ---")
    for log_entry in bank_log:
        print(log_entry)
    print("\n--- End of Session ---")

while True:
    choice = input(menu)

    if choice == "n":
        taxid = input("Enter your Tax ID:\n")
        name = input("Enter your name:\n")
        create_new_account(name, taxid)
        current_customer = set_current_user(taxid)

    elif choice == "l":
        if current_customer:
            print("You are already logged in. Log out first if you want to switch accounts.")
        else:
            taxid = input("Enter your Tax ID to login:\n")
            current_customer = set_current_user(taxid)
            if current_customer:
                print(f"Logged in as {current_customer.name}")

    elif choice == "o":
        if current_customer:
            print(f"Logging out of {current_customer.name}'s account.")
            current_customer = None
        else:
            print("No account is currently logged in.")

    elif choice == "d" and current_customer:
        dep = abs(int(input("How much do you want to deposit? (e.g., 1000)\n")))
        current_customer.deposit(dep)

    elif choice == "w" and current_customer:
        withdrawal = abs(int(input("How much do you want to withdraw? (e.g., 500)\n")))
        current_customer.withdraw(withdrawal)

    elif choice == "s" and current_customer:
        current_customer.show_statement()

    elif choice == "e":
        print_final_log()
        break

    else:
        print("Invalid operation or no account logged in. Please select a valid option.")
    
    if current_customer and not want_to_continue():
        print_final_log()
        break