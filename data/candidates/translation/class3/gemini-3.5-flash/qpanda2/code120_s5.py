# EVAL_META: task_id=120, framework=qpanda2, class=3
import math
from pyqpanda import *

# Initialize CPUQVM and qAlloc_many at the global scope
machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(20)

def create_diagonal_circuit(diag):
    n_qubits = int(math.log2(len(diag)))
    qubits = global_qubits[:n_qubits]
    
    prog = QProg()
    complex_diag = [complex(x) for x in diag]
    
    gate = DiagonalGate(qubits, complex_diag)
    prog.insert(gate)
    
    return prog

machine.finalize()
