# EVAL_META: task_id=58, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import *
import numpy as np

# Global QVM initialization
machine = init_quantum_machine(QMachineType.CPU)
qubits = machine.qAlloc_many(2)

def create_ch_gate():
    circuit = QCircuit()
    circuit << RY(qubits[1], np.pi/4) \
            << CNOT(qubits[0], qubits[1]) \
            << RY(qubits[1], -np.pi/4)
    return circuit

# Manual Cleanup
machine.finalize()
