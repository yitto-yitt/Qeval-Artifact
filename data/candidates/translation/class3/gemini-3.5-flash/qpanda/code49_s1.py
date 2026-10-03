# EVAL_META: task_id=49, framework=qpanda, class=3
import pyqpanda3.core as pq

def simple_elitzur_vaidman():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1]) << pq.H(qubits[0])
    return prog
