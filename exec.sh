#!/bin/bash

. venv/bin/activate

cd gymces_payments || return
python3 "$1.py"

deactivate