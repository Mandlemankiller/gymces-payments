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
    missing: List[str] = payment['people'].copy()
    paid: List[str] = []
    incorrect: List[str] = []

    amount_collected: float = 0
    amount_total: float = payment['amount'] * len(payment['people'])

    csv_folder_path: str = '../data/csv'

    csv_name_input: str = input('CSV export file path (leave empty for most recent from CSV data): ')
    if csv_name_input == '':
        files: List[str] = os.listdir(csv_folder_path)
        csvs: List[str] = [file for file in files if file.endswith('.csv')]
        if not csvs:
            fatal('There are no .csv files to choose from!')
        timestamps: Dict[str, float] = {}

        for csv_file in csvs:
            csv_path = os.path.join(csv_folder_path, csv_file)
            timestamp: float = os.path.getmtime(csv_path)
            timestamps[csv_path] = timestamp
        csv_path: str = max(timestamps, key=timestamps.get)
        print(f'Using {os.path.basename(csv_path)} for CSV file')
    else:
        csv_path: str = csv_name_input.replace('file://', '')
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
            amount_collected += grouped_amount
            if grouped_amount != payment['amount']:
                warning(f'{account_name} paid incorrect amount ({grouped_amount} CZK)!')
                if account_name in missing:
                    missing.remove(account_name)
                incorrect.append(account_name + f' ({grouped_amount} CZK)')
                paid.append('\033[1;33m' + account_name + '\033[0;32m')
            else:
                if account_name in missing:
                    missing.remove(account_name)
                else:
                    warning(f'{account_name} was not supposed to pay!')
                paid.append(account_name)

    for account_name in payment['cash']:
        missing.remove(account_name)
        paid.append('\033[0;34m' + account_name + '\033[0;32m')

    EQ: int = 800
    print('=' * EQ)
    print(f'\033[1;35m{payment["title"].upper()}\033[0m\n')
    print(f'\033[1;36mTotal:\033[0m')
    print(f'\033[0;36m{len(payment["people"])} people\033[0m')
    print(
        f'\033[0;36m{amount_collected}/{amount_total} CZK collected'
        f' ({round(amount_collected / amount_total * 100, 2)}%)\033[0m\n'
    )
    print(f'\033[1;32mPaid ({len(paid)}): \033[0;32m[' + ', '.join(paid) + ']\033[0m')
    print(f'\033[1;33mIncorrect ({len(incorrect)}): \033[0;33m[' + ', '.join(incorrect) + ']\033[0m')
    print(f'\033[1;31mMissing ({len(missing)}): \033[0;31m[' + ', '.join(missing) + ']\033[0m')
    print('=' * EQ)
