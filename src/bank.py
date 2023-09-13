# menu.py

import os
import pickle
import re
from account import Account


def is_valid_phone(phone):
    # 验证手机号的正则表达式
    phone_pattern = re.compile(r'^[1-9][0-9]{10}$')
    return phone_pattern.match(phone) is not None

def create_account():
    account_number = input("输入账户号码: ")

    # 验证姓名是否为空
    if not account_number:
        print("账户号码不可为空.")
        return
    
    # 检查账户是否已存在
    if load_account(account_number):
        print("账户已存在.")
        return
    
    account_name = input("输入姓名:")

    # 验证姓名是否为空
    if not account_name:
        print("账户姓名不可为空.")
        return

    password = input("设置密码: ")

    phone = input("输入手机号: ")

    # 验证手机号是否合法
    if not is_valid_phone(phone):
        print("不合法的格式. 请输入有效的11位手机号码:")
        return

    # 救援码
    rescue_code = input("请输入五位救援码:")    
    # 开户时设置余额为0
    balance = 0.0
    account = Account(account_number, account_name, password, phone, balance, rescue_code)
    save_account(account)
    print("开户成功.")

def save_account(account):
    with open(f"{account.account_number}.dat", "wb") as file:
        pickle.dump(account, file)

def load_account(account_number):
    try:
        with open(f"{account_number}.dat", "rb") as file:
            account = pickle.load(file)
            return account
    except FileNotFoundError:
        return None

# 更新账户信息
def modify_account(account):
    if account.is_suspended:
            print("账户已挂失，无法进行该操作。")
            return

    print(f"账户信息:\n{account}")
    new_name = input("输入新的账户名 (Press Enter to keep current name): ")
    new_password = input("设置新的密码 (Press Enter to keep current password): ")
    new_phone = input("输入新的手机号 (Press Enter to keep current phone number): ")

    if new_name:
        account.account_name = new_name
    if new_password:
        account.password = new_password
    if new_phone:
        account.phone = new_phone

    save_account(account)
    print("账户信息更新成功.")

# 销户
def close_account(account):
    # 挂失状态下无法销户
    if account.is_suspended:
            print("账户已挂失，无法进行该操作。")
            return

    confirmation = input("警告，该操作无法撤销! 确认要销户吗? (输入 'yes' 确认): ")
    
    if confirmation.lower() == 'yes':
        password_attempt = input("请输入密码以确认销户: ")
        
        
        if password_attempt == account.password:
            os.remove(f"{account.account_number}.dat")
            print("成功销户.")
        else:
            print("密码错误，销户失败.")
    else:
        print("销户操作已取消.")

# 挂失
def report_loss(account):
    confirmation = input("警告，确认要挂失吗? (输入 'yes' 确认): ")

    if confirmation.lower() == 'yes':
        password_attempt = input("请输入密码以确认挂失: ")
        # 校验密码
        if password_attempt == account.password:
            account.is_suspended = True
            print(f"账户 {account.account_number} 已挂失.")
        else:
            print("密码错误，挂失失败.")
    else:
        print("挂失操作已取消.")

# 主界面
def main_menu():
    while True:
        print("\n----------------------------")
        print("Bank Savings Management System")
        print("1. 开户")
        print("2. 登录账户")
        print("3. 退出系统")
        choice = input("选择一个项目: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            account_number = input("输入账户号码: ")
            account = load_account(account_number)
            if account:
                password = input("输入账户密码: ")
                if password == account.password:
                    account_menu(account)
                else:
                    print("密码错误.")
            else:
                print("账户不存在.")
        elif choice == "3":
            break
        else:
            print("无效选项. 请重试.")

# 业务菜单
def account_menu(account):
    while True:
        # Account Menu
        print("--------------------")
        print("\n业务菜单")
        print("1. 存款")
        print("2. 取款")
        print("3. 查询余额")
        print("4. 修改帐户信息")
        print("5. 销户")
        print("6. 挂失")
        print("7. 交易历史记录")
        print("8. 账户救援")
        print("9. 退出登录")
        choice = input("Select an option: ")

        if choice == "1":
            amount = float(input("输入存款金额: "))
            account.deposit(amount)
            print(f"New balance: {account.get_balance()}")
        elif choice == "2":
            amount = float(input("输入取款金额: "))
            account.withdraw(amount)
            print(f"New balance: {account.get_balance()}")
        elif choice == "3":
            print(f"Current balance: {account.get_balance()}")
        elif choice == "4":
            modify_account(account)
        elif choice == "5":
            close_account(account)
            break
        elif choice == "6":
            report_loss(account)
        elif choice == "7":
            transactions = account.get_transaction_history()
            if transactions:
                print("\n交易历史记录:")
                for transaction in transactions:
                    print(transaction)
            else:
                print("没有交易历史记录.")
        elif choice == "8":
            if account.is_suspended:
                account.cancel_suspension()
            else:
                print("账户没有挂失状态，无需使用救援码。")
        elif choice == "9":
            break
        else:
            print("无效选项. 请重新输入.")