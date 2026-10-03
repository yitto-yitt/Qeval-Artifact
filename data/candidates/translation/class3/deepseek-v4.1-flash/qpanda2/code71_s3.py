# EVAL_META: task_id=71, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    circuit = QCircuit()
    circuit << H(qubits[0])
    rx_gate = RX(qubits[1], np.pi / 2)
    rx_gate.setControl([qubits[0]])
    circuit << rx_gate
    circuit << U1(qubits[0], np.pi / 4)
    circuit << H(qubits[1])
    return circuit

machine.finalize()
