# EVAL_META: task_id=70, framework=qpanda2, class=3
import pyqpanda as pq

# Initialize global QVM and qubits
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.SWAP(q[1], q[2]).control([q[0]])
    prog << pq.H(q[1])
    prog << pq.Sdg(q[0]).control([q[1]])
    return prog

machine.finalize()
