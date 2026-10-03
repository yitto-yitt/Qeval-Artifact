# EVAL_META: task_id=71, framework=qpanda2, class=3
from pyqpanda import *
import math

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    circ = QCircuit()
    circ << H(qubits[0])
    circ << H(qubits[1])
    circ << RZ(qubits[1], math.pi / 4)
    circ << CNOT(qubits[0], qubits[1])
    circ << RZ(qubits[1], -math.pi / 4)
    circ << CNOT(qubits[0], qubits[1])
    circ << U1(qubits[0], math.pi / 4)
    return circ

machine.finalize()
