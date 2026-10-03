# EVAL_META: task_id=70, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    prog = pq.QProg()
    
    prog << pq.H(qubits[0])
    prog << pq.SWAP(qubits[1], qubits[2]).control([qubits[0]])
    prog << pq.H(qubits[1])
    prog << pq.S(qubits[0]).dagger().control([qubits[1]])
    
    return prog
