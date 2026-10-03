# EVAL_META: task_id=38, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init()
qubits = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CRZ(qubits[0], qubits[1], theta)
    prog << pq.H(qubits[1])
    prog << pq.CRY(qubits[1], qubits[0], theta)
    return prog

machine.finalize()
