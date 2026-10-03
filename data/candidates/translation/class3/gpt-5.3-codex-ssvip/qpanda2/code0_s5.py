# EVAL_META: task_id=0, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def create_quantum_circuit(n_qubits):
    q = machine.qAlloc_many(n_qubits)
    prog = pq.QProg()
    return prog

machine.finalize()
