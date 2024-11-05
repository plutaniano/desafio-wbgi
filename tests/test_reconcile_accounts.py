import csv

from src.reconcile_accounts import reconcile_accounts
from tests import ARTIFACTS


def test_default():
    txs1 = list(csv.reader((ARTIFACTS / "transactions1.csv").open()))
    txs2 = list(csv.reader((ARTIFACTS / "transactions2.csv").open()))

    out1, out2 = reconcile_accounts(txs1, txs2)

    assert out1 == [
        ["2020-12-04", "Jurídico", "60.00", "LinkSquares", "FOUND"],
        ["2020-12-04", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
        ["2020-12-05", "Tecnologia", "50.00", "AWS", "MISSING"],
    ]

    assert out2 == [
        ["2020-12-04", "Jurídico", "60.00", "LinkSquares", "FOUND"],
        ["2020-12-04", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
        ["2020-12-05", "Tecnologia", "49.99", "AWS", "MISSING"],
    ]
