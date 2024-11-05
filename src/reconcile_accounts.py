import copy
import datetime as dt
from typing import List, Optional, Tuple

Tx = List[str]
Txs = List[Tx]


def _reconcile_tx(tx: Tx, txs: Txs, pivot: int) -> Tuple[int, Optional[Tx]]:
    "Procura `tx` em `txs` começando pelo índice `pivot`"

    tx_date_str, *tx_fields = tx
    tx_date = dt.date.fromisoformat(tx_date_str)
    tx_date_min = tx_date - dt.timedelta(days=1)
    tx_date_max = tx_date + dt.timedelta(days=1)
    tx_date_range = [tx_date_min, tx_date, tx_date_max]

    while pivot != 0:
        txs_date_str, *_ = txs[pivot]
        txs_date = dt.date.fromisoformat(txs_date_str)
        if txs_date <= tx_date_min:
            pivot -= 1
        else:
            break

    for candidate in txs[pivot:]:
        txs_date_str, *txs_fields = candidate
        txs_date = dt.date.fromisoformat(txs_date_str)

        if txs_date not in tx_date_range:
            return pivot, None

        if tx_fields == txs_fields:
            return pivot, candidate

        pivot += 1
    return pivot, None


def reconcile_accounts(txs1: Txs, txs2: Txs) -> Tuple[Txs, Txs]:
    txs1 = copy.deepcopy(txs1)
    txs2 = copy.deepcopy(txs2)

    txs1.sort()
    txs2.sort()

    pivot = 0
    for tx in txs1:
        pivot, match = _reconcile_tx(tx, txs2, pivot)
        if match:
            tx.append("FOUND")
            match.append("FOUND")
        else:
            tx.append("MISSING")

    # Processa a segunda lista de transações para encontrar itens sem correspondência
    for tx2 in txs2:
        if tx2[-1] not in ["MISSING", "FOUND"]:
            tx2.append("MISSING")

    return txs1, txs2
