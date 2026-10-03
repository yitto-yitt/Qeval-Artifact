# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep(num_qubits):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)

    prog = pq.QProg()
    if num_qubits > 0:
        prog.insert(pq.X(qubits[0]))
        for i in range(1, num_qubits):
            prog.insert(pq.RZ(qubits[i], 0.0))

    if not hasattr(create_state_prep, "_resources"):
        create_state_prep._resources = []
    create_state_prep._resources.append((qvm, qubits))

    return prog
