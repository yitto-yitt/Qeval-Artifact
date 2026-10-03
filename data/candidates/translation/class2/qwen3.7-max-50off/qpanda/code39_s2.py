# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit, QMachine

def create_uniform_superposition(n):
    qvm = QMachine()
    qubits = qvm.alloc_qubits(n)
    qc = QuantumCircuit()
    for q in qubits:
        qc.h(q)
    qvm.apply(qc)
    return qvm.get_statevector()
