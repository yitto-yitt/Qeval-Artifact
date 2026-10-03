# EVAL_META: task_id=70, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    circ = QCircuit()
    circ << H(qubits[0])
    circ << CSWAP(qubits[0], qubits[1], qubits[2])
    circ << H(qubits[1])
    circ << CU1(qubits[1], qubits[0], -PI/2)
    return circ

machine.finalize()
