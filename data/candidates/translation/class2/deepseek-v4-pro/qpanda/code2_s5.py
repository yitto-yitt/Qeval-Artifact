# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit, QProg, H, CNOT, statevector


def create_bell_statevector():
    qc = QuantumCircuit(2)
    qc << H(0) << CNOT(0, 1)
    prog = QProg(qc)
    return statevector(prog)
