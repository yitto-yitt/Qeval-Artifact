# EVAL_META: task_id=120, framework=qpanda2, class=3
import pyqpanda as pq
import math

machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(20)

def create_diagonal_circuit(diag):
    n = int(math.log2(len(diag)))
    qubits = global_qubits[:n]
    prog = pq.QProg()
    diag_complex = [complex(x) for x in diag]
    gate = pq.diagonal_gate(qubits, diag_complex)
    prog << gate
    return prog

machine.finalize()
