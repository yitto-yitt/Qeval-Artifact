# EVAL_META: task_id=69, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CS(qubits[0], qubits[1]) << pq.H(qubits[1]) << pq.CSdag(qubits[1], qubits[0])
    return prog
