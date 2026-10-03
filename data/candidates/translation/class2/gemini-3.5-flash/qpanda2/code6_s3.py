# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq

def create_state_prep(num_qubits):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    prog = pq.QProg()
    prog << pq.X(qubits[0])
    prog._machine = machine  # Keep machine alive to prevent garbage collection of qubits
    return prog
