# EVAL_META: task_id=120, framework=qpanda, class=3
import pyqpanda3.core as pq
import math

_global_machine = None

def _get_machine():
    global _global_machine
    if _global_machine is None:
        _global_machine = pq.CPUQVM()
        _global_machine.init_qvm()
    return _global_machine

def create_diagonal_circuit(diag):
    machine = _get_machine()
    num_qubits = int(math.log2(len(diag)))
    qubits = machine.qAlloc_many(num_qubits)
    prog = pq.QProg()
    prog << pq.DiagonalGate(qubits, [complex(x) for x in diag])
    return prog
