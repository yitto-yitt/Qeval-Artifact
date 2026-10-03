# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep(num_qubits):
    if not hasattr(create_state_prep, "_qvm"):
        create_state_prep._qvm = pq.CPUQVM()
        create_state_prep._qvm.init_qvm()

    qvm = create_state_prep._qvm
    qubits = qvm.qAlloc_many(num_qubits)
    prog = pq.QProg()

    if num_qubits > 0:
        prog.insert(pq.X(qubits[0]))
        for i in range(1, num_qubits):
            prog.insert(pq.H(qubits[i]))
            prog.insert(pq.H(qubits[i]))

    return prog
