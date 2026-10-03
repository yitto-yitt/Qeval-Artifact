# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def inv_circuit(n):
    qc = QuantumCircuit(n)
    # Original circuit: H(1), H(2), CNOT(1,3), CNOT(2,4).
    # H and CNOT are self-inverse, so the inverse is the reversed sequence.
    qc.cnot(2, 4)
    qc.cnot(1, 3)
    qc.h(2)
    qc.h(1)
    return qc
