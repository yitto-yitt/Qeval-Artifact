# EVAL_META: task_id=62, framework=qpanda2, class=2
import pyqpanda as pq


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)
    prog = pq.QProg()
    for i in range(len(basis)):
        if state[i] == 1:
            prog << pq.X(qubits[i])
        if basis[i] == 1:
            prog << pq.H(qubits[i])
    return prog
