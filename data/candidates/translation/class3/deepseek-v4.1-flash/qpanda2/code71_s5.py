# EVAL_META: task_id=71, framework=qpanda2, class=3
from pyqpanda import *
import math

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << U1(qubits[0], math.pi / 4)
    circuit << CRX(qubits[0], qubits[1], math.pi / 2)
    circuit << H(qubits[1])
    return circuit

machine.finalize()
