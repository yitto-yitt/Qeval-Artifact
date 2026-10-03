# EVAL_META: task_id=59, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_cz_gate():
    prog = pq.QProg()
    prog.insert(pq.H(qubits[1]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.H(qubits[1]))
    return prog

machine.finalize()
