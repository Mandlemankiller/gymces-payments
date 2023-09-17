from typing import *
import json
from common import *

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

    names: List[str] = [s.strip() for s in input('Paid cash: ').split(',')]
    payment: Dict = payments[check_id]

    for name in names:
        if name not in accounts:
            fatal(f'Person {name} does not exist!')
        if name in payment['cash']:
            fatal(f'Person {name} already paid cash!')

    payment['cash'].extend(names)

    with open('../data/payments.json', 'w') as file:
        json.dump(payments, file, ensure_ascii=False)
