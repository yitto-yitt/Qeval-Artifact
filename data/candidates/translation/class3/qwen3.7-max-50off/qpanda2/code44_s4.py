# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def tensor_circuits():
    prog = pq.QProg()
    # Decomposition of CRY(0.2) controlled by qubit 0, targeting qubit 1
    prog << pq.RY(qubits[1], 0.1)
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.RY(qubits[1], -0.1)
    prog << pq.CNOT(qubits[0], qubits[1])
    
    # X gate on qubit 2 (the tensored 1-qubit circuit)
    prog << pq.X(qubits[2])
    return prog

machine.finalize()
