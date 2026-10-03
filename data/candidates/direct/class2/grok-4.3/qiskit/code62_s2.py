# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit
def bb84_senders_circuit(state, basis):
    qc = QuantumCircuit(1)
    if state == 1:
        qc.x(0)
    if basis == 1:
        qc.h(0)
    return qc
