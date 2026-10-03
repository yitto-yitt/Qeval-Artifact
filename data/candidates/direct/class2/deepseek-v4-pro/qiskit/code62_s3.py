# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis):
    if len(state) != len(basis):
        raise ValueError("state and basis must have the same length")
    n = len(state)
    qc = QuantumCircuit(n)
    for idx, (s, b) in enumerate(zip(state, basis)):
        if int(s) == 1:
            qc.x(idx)
        if int(b) == 1:
            qc.h(idx)
    return qc
