# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq

def create_state_prep(num_qubits):
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = qvm.qAlloc_many(num_qubits)
    prog = pq.QProg()
    prog << pq.X(qubits[0])
    return prog
