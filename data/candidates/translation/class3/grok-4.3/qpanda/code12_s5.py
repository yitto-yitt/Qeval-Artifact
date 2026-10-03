# EVAL_META: task_id=12, framework=qpanda, class=3
import pyqpanda3.core as pq

def get_unitary():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    return qvm.get_unitary_matrix(prog)
