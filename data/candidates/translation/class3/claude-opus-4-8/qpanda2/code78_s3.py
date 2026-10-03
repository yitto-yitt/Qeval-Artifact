# EVAL_META: task_id=78, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)


def qft_no_swaps(num_qubits):
    qlist = [qubits[i] for i in range(num_qubits)]
    circuit = pq.QCircuit()

    # Inverse of QFT (do_swaps=False) built by reversing and daggering the forward QFT
    # Forward QFT (no swaps): for j in range(n): H(q[j]); for k in j+1..n-1: CP(pi/2^(k-j)) control k target j
    forward = pq.QCircuit()
    for j in range(num_qubits):
        forward << pq.H(qlist[j])
        for k in range(j + 1, num_qubits):
            angle = np.pi / (2 ** (k - j))
            forward << pq.CR(qlist[k], qlist[j], angle)

    circuit << forward.dagger()
    return circuit


prog = pq.QProg()
prog << qft_no_swaps(3)
machine.finalize()
