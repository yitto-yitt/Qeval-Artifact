# EVAL_META: task_id=120, framework=qpanda2, class=3
import pyqpanda as pq
import math

# Initialize global QVM and allocate qubits
machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(16)

def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    qubits = global_qubits[:num_qubits]
    
    prog = pq.QProg()
    diag_complex = [complex(x) for x in diag]
    diag_circ = pq.diagonal_gate(qubits, diag_complex)
    prog.insert(diag_circ)
    return prog

# Manual Cleanup
machine.finalize()
