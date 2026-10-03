# EVAL_META: task_id=59, framework=qpanda, class=3
import pyqpanda3.core as pq

# Initialize the quantum virtual machine globally to keep qubits and program valid
_machine = pq.CPUQVM()
_machine.init_qvm()

def create_cz_gate():
    q = _machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[1]) << pq.CNOT(q[0], q[1]) << pq.H(q[1])
    return prog
