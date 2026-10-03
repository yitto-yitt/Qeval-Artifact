# EVAL_META: task_id=120, framework=qpanda2, class=3
import math
from pyqpanda import *

# Initialize global QVM and allocate qubits
machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(20)

def create_diagonal_circuit(diag):
    num_qubits = int(round(math.log2(len(diag))))
    qubits = global_qubits[:num_qubits]
    
    circuit = QCircuit()
    diag_gate = diagonal_gate(qubits, diag)
    circuit << diag_gate
    return circuit

machine.finalize()
