# EVAL_META: task_id=0, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(1024)

def create_quantum_circuit(n_qubits):
    prog = pq.QProg()
    return prog

machine.finalize()
