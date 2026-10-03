# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep(num_qubits):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(num_qubits)
    prog = pq.QProg()
    
    # Prepare state |1> which means all qubits should be in |1>
    for qubit in qubits:
        prog << pq.X(qubit)
    
    return prog
