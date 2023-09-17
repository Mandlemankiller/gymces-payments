import json
from typing import *
from common import *
import os
import csv

if __name__ == '__main__':
    with open('../data/payments.json', 'r') as file:
        payments: List[Dict] = json.load(file)

    with open('../data/accounts.json', 'r') as file:
        accounts: Dict[str, List[str]] = json.load(file)

    check_id_input: str = input('Check id (leave empty for last): ')
    check_id: int = 0
    if check_id_input == '':
        check_id = payments[len(payments) - 1]['id']
        print(f'Using {check_id} for check id')
    else:
        try:
            check_id = int(check_id_input)
        except ValueError:
            fatal('Invalid id value!')

    payment: Dict = payments[check_id]
    unpaid: List[str] = list(payment['people'])
    paid: List[str] = []
    incorrect: List[str] = []
    cash: List[str] = []

    csv_path: str = input('CSV export file path: ')
    csv_path = csv_path.replace('file://', '')
    if not os.path.exists(csv_path):
        fatal('That file does not exist!')

    with open(csv_path, 'r', newline='', encoding='cp1250') as file:
        reader: csv.DictReader = csv.DictReader(file, delimiter=';')

        grouped_payments: Dict[str, float] = {}

        for row in reader:
            if row['Variabilní symbol'] == payment['variable']:
                account_number: str = row['Číslo účtu protistrany']
                name: str = account_number
                for person, payment_accounts in accounts.items():
                    if account_number in payment_accounts:
                        name = person

                paid_amount: float = float(row['Částka v měně účtu'].replace(',', '.'))
                if name in grouped_payments.keys():
                    grouped_payments[name] = grouped_payments[name] + paid_amount
                else:
                    grouped_payments[name] = paid_amount

                if name == account_number:
                    warning(f'Unknown account number {account_number} with name {row["Název účtu protistrany"]}')

        for account_name, grouped_amount in grouped_payments.items():
            if grouped_amount != payment['amount']:
                warning(f'{account_name} paid incorrect amount ({grouped_amount} CZK)!')
                unpaid.remove(account_name)
                incorrect.append(account_name + f' ({grouped_amount} CZK)')
            else:
                if account_name in unpaid:
                    unpaid.remove(account_name)
                else:
                    warning(f'{account_name} was not supposed to pay!')
                paid.append(account_name)

        for account_name in payment['cash']:
            unpaid.remove(account_name)
            cash.append(account_name)

    print('==================================================================')
    print(f'\033[1;36mTotal people: \033[0;36m{len(payment["people"])}\033[0m\n')
    print(f'\033[1;32mPaid ({len(paid)}): \033[0;32m[' + ', '.join(paid) + ']\033[0m')
    print(f'\033[1;34mCash ({len(cash)}): \033[0;34m[' + ', '.join(cash) + ']\033[0m')
    print(f'\033[1;33mIncorrect ({len(incorrect)}): \033[0;33m[' + ', '.join(incorrect) + ']\033[0m')
    print(f'\033[1;31mUnpaid ({len(unpaid)}): \033[0;31m[' + ', '.join(unpaid) + ']\033[0m')
    print('==================================================================')
