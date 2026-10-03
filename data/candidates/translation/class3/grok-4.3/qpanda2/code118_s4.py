# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
machine = CPUQVM()
machine.initQVM()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    circuit = QCircuit()
    sx_matrix = np.array([[0.5+0.5j, 0.5-0.5j], [0.5-0.5j, 0.5+0.5j]])
    c3sx = QOracle([qubits[3]], sx_matrix).control([qubits[0], qubits[1], qubits[2]])
    circuit << c3sx
    return circuit

machine.finalize()
