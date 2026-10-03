# EVAL_META: task_id=120, framework=qpanda, class=3
import pyqpanda3.core as pq
import math

_keep_alive = []

def create_diagonal_circuit(diag):
    global _keep_alive
    n_qubits = int(math.log2(len(diag)))
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n_qubits)
    
    prog = pq.QProg()
    gate = pq.DiagonalGate(qubits, diag)
    prog.insert(gate)
    
    _keep_alive.append((machine, qubits))
    return prog
