# account.py

import datetime

class Account:
    def __init__(self, account_number, account_name, password, phone, balance, rescue_code):
        self.account_number = account_number
        self.account_name = account_name
        self.password = password
        self.phone = phone
        self.balance = balance
        self.transactions = []
        self.is_suspended = False  # 添加挂失状态属性
        self.rescue_code = rescue_code  # 添加救援码属性

    def deposit(self, amount):
        if self.is_suspended:
            print("账户已挂失，无法进行存款操作。")
            return
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"存款: +{amount} on {datetime.datetime.now()}")

    def withdraw(self, amount):
        if self.is_suspended:
            print("账户已挂失，无法进行存款操作。")
            return
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"取款: -{amount} on {datetime.datetime.now()}")

    def get_balance(self):
        return self.balance

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transaction_history(self):
        return self.transactions

    def __str__(self):
        return f"账户号码: {self.account_number}, 账户名: {self.account_name}, 余额: {self.balance}"
    
    def cancel_suspension(self):
        if self.is_suspended:
            rescue_attempt = input("输入救援码以取消挂失状态: ")
            if rescue_attempt == self.rescue_code:
                self.is_suspended = False
                print("账户挂失状态已取消。")
            else:
                print("救援码错误，无法取消挂失状态。")