# EVAL_META: task_id=89, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_controlled_hgate():
    prog = pq.QProg()
    h_gate = pq.H(qubits[2])
    cch_gate = h_gate.control([qubits[0], qubits[1]])
    prog << cch_gate
    return prog

machine.finalize()
