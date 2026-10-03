# EVAL_META: task_id=106, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def compose_cnot_dihedral():
    prog = pq.QProg()
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.T(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.T(qubits[0])
    prog << pq.X(qubits[1])
    return prog

machine.finalize()
