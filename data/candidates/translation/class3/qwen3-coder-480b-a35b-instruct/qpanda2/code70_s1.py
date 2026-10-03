# EVAL_META: task_id=70, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CSWAP(qubits[0], qubits[1], qubits[2])
    prog << pq.H(qubits[1])
    prog << pq.CSdag(qubits[1], qubits[0])
    return prog

machine.finalize()
