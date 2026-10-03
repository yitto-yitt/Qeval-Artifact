# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep(num_qubits):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    
    prog = pq.QProg()
    # To prepare state |1>, we need to apply X gate to all qubits initially in |0>
    for qubit in qubits:
        prog << pq.X(qubit)
    
    return prog
