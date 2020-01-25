from dataBase import Database


class User:

    def __init__(self, first_name, last_name, passport_id, email, password, is_admin, join_date, account_balance):
        self.first_name = first_name
        self.last_name = last_name
        self.passport_id = passport_id
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.join_date = join_date
        self.account_balance = account_balance
