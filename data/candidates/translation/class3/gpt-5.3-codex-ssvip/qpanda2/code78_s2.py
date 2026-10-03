# EVAL_META: task_id=78, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def qft_no_swaps(num_qubits):
    qubits = _global_qubits[:num_qubits]
    prog = pq.QProg()
    for j in range(num_qubits):
        for k in range(j):
            angle = -3.141592653589793 / (2 ** (j - k))
            prog.insert(pq.CR(qubits[j], qubits[k], angle))
        prog.insert(pq.H(qubits[j]))
    machine.directly_run(prog)
    return prog

machine.finalize()
