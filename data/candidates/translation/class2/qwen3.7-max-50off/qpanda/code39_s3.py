# EVAL_META: task_id=39, framework=qpanda, class=2
import pyqpanda3.core as pq3

def create_uniform_superposition(n):
    qm = pq3.init_quantum_machine(pq3.QuantumMachineType.CPU)
    q = qm.qAlloc_many(n)
    prog = pq3.QProg()
    for i in range(n):
        prog << pq3.H(q[i])
    return qm.get_statevector(prog)
