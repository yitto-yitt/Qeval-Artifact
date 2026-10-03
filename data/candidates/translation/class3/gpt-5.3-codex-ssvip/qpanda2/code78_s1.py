# EVAL_META: task_id=78, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def qft_no_swaps(num_qubits):
    qubits = _global_qubits[:num_qubits]
    prog = pq.QProg()
    for j in range(num_qubits):
        prog << pq.H(qubits[j])
        for k in range(j + 1, num_qubits):
            angle = -3.141592653589793 / (2 ** (k - j))
            prog << pq.CR(qubits[k], qubits[j], angle)
    machine.directly_run(prog)
    machine.finalize()
    return prog
