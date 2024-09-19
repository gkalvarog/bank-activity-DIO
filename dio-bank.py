'''
Requirements:

1. Deposit: only positive amounts, added to one variable and shown on the statement (assign a variable)
2. Withdrawal: up to 3 daily withdrawals, each of 500. If not enough balance, pop up message (not enough balance), added to one variable and shown on the statement (assign a variable)
3. Statement: display balance as a format "R$ {balance}"
'''

menu = """
[d] Deposit
[w] Withdraw
[s] Statement
[e] Exit
=> """

balance = 0
limit = 500
statement = []
max_amount_withdrawal = balance
number_withdrawals = 0
LIMIT_WITHDRAWAL = 3


while True:

    choice = input(menu)

    if choice == "d":
        deposit = abs(int(input("How much you desire to deposit? Write the amount in number notation, ex: 1000.\n")))
        balance += deposit
        statement.append(deposit)

        # updating the maxmim amount of withdrawal on a given day, as we cannot say that 2000 can be withdrawn even if there are 1500+ in the account.
        if balance > 1500:
            max_amount_withdrawal = 1500

        # ask if wants to continue making transactions
        new_op = input(f"Your balance is R$ {balance}. Would you like to make a new operation?\n")
        
        if new_op[0].lower() == "n":
            break

    elif choice == "w":
        if number_withdrawals < LIMIT_WITHDRAWAL:

            withdrawal = abs(int(input("How much you desire to withdraw? Write the amount in number notation, ex: 500.\n")))

            if balance >= withdrawal:

                if withdrawal <= 500:
                    
                    balance -= withdrawal
                    statement.append(-withdrawal)

                    number_withdrawals += 1

                    # updating the maxmim amount of withdrawal on a given day, as we cannot say that 1200 can be withdrawn if 1 withdrawal has already happened.
                    max_amount_withdrawal = (LIMIT_WITHDRAWAL - number_withdrawals) * 500

                    # ask if wants to continue making transactions
                    new_op = input(f"Your balance is R$ {balance}. Would you like to make a new operation?\n")
                    
                    if new_op[0].lower() == "n":
                        break
                
                else:
                    print("You can withdraw up to R$ 500 per time. Repeat the operation.")

            else:
                print(f"There is not enough balance to complete this transaction. At this moment, you can withdraw up to R$ {max_amount_withdrawal}. Repeat the operation.")

        else:
            print(f"You can withdraw up to {LIMIT_WITHDRAWAL} times per day. Try again tomorrow.")
            break

    elif choice == "s":
        print(f"Your balance is R$ {balance}. This is the history of your transactions: {statement}.")
        
        # ask if wants to continue making transactions
        new_op = input(f"Would you like to make a new operation?\n")
                    
        if new_op[0].lower() == "n":
            break

    elif choice == "e":
        break

    else:
        print("Invalid operation. Please select a valid operation.")