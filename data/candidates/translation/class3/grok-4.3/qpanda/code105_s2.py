# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QCircuit, CNOT, T, QProg

def initialize_cnot_dihedral():
    qm = QuantumMachine()
    qubits = qm.allocate_qubits(2)
    circ = QCircuit()
    circ << CNOT(qubits[0], qubits[1])
    circ << T(qubits[0])
    prog = QProg()
    prog << circ
    return prog
