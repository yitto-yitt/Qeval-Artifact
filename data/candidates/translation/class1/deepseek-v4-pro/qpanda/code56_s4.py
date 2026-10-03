# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import init_qvm, finalize_qvm, qAlloc_many, QProg, X, prob_run_dict

def not_gate(a):
    init_qvm()
    try:
        qubits = qAlloc_many(8)
        prog = QProg()
        bits = format(a, "08b")
        for i in range(8):
            if bits[7 - i] == "0":
                prog << X(qubits[i])
        dist = prob_run_dict(prog, list(reversed(qubits)))
    finally:
        finalize_qvm()
    total = sum(dist.values())
    return {bitstring: prob / total for bitstring, prob in dist.items()}
