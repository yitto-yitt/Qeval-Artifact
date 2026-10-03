# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import *

def create_unitary_from_matrix():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    
    matrix = [
        0, 0, 0, 1,
        0, 0, 1, 0,
        1, 0, 0, 0,
        0, 1, 0, 0
    ]
    matrix_complex = [complex(x) for x in matrix]
    
    gate = matrix_to_gate(matrix_complex, qubits)
    circuit = QCircuit()
    circuit << gate
    return circuit
