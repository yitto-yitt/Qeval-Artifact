# EVAL_META: task_id=57, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_swap_gate():
    prog = pq.QProg()
    prog << pq.CX(qubits[0], qubits[1]) << pq.CX(qubits[1], qubits[0]) << pq.CX(qubits[0], qubits[1])
    return prog

machine.finalize()
