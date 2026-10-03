# EVAL_META: task_id=130, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1000)

def inv_circuit(n):
    prog = pq.QProg()
    prog << pq.CNOT(qubits[2], qubits[4])
    prog << pq.CNOT(qubits[1], qubits[3])
    prog << pq.H(qubits[2])
    prog << pq.H(qubits[1])
    return prog

machine.finalize()
