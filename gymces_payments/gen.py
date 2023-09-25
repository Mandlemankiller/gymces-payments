from datetime import datetime

from qr.spayd import QRPaymentGenerator
from qr.svg import QRPaymentSVGImage
from transformer import gen_png
from typing import *
import json
from common import *
import os


def gen_variable_symbol() -> str:
    return datetime.now().strftime('%y%m%d') + id_str


if __name__ == '__main__':
    with open('../data/payments.json', 'r') as file:
        payments: List[Dict] = json.load(file)

    with open('../data/groups.json', 'r') as file:
        groups: Dict[str, List[str]] = json.load(file)

    with open('../data/accounts.json', 'r') as file:
        accounts: Dict[str, List[str]] = json.load(file)

    with open('../data/config.json', 'r') as file:
        config: Dict[str, str] = json.load(file)

    with open('../data/qrs.json', 'r') as file:
        qrs: Dict[int, str] = json.load(file)

    if len(payments) == 0:
        last_id: int = -1
    else:
        last_id: int = payments[len(payments) - 1]['id']
    id_str: str = f'{last_id + 1:04}'

    iban: str = config['iban']

    title: str = input('Title: ')
    amount: float = 0
    try:
        amount = float(input('Amount: '))
    except ValueError:
        fatal('Invalid amount value!')
    people_input: str = input('People / Group: ')
    if people_input in groups.keys():
        people: List[str] = groups[people_input]
    else:
        people: List[str] = [s.strip() for s in people_input.split(',')]
    for person in people:
        if person not in accounts:
            fatal('Person ' + person + ' does not exist!')
    currency: str = 'CZK'
    variable_symbol: str = gen_variable_symbol()

    generator: QRPaymentGenerator = QRPaymentGenerator(
        account=iban,
        amount=amount,
        currency=currency,
        x_vs=variable_symbol,
        message=title,
    )

    amount_desc: str = f'{amount:.2f}'.replace('.', ',')

    image: QRPaymentSVGImage = generator.make_image(
        title=title,
        amount=amount_desc + ' ' + currency,
        box_size=20,
        border=4
    )

    if not os.path.exists('../target/'):
        os.mkdir('../target')

    img_path: str = f'../target/{int(id_str)}_{title}.svg'

    image.save(img_path)
    gen_png(img_path)

    with open('../data/payments.json', 'w') as file:
        payments.append({
            "id": int(id_str),
            "title": title,
            "amount": amount,
            "people": people,
            "cash": [],
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "variable": variable_symbol
        })
        json.dump(payments, file, ensure_ascii=False)

    with open('../data/qrs.json', 'w') as file:
        qrs[int(id_str)] = str(image.to_string())
        json.dump(qrs, file, ensure_ascii=False)
