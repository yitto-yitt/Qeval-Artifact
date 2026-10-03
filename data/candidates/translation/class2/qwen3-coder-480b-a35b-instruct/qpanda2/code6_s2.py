# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep(num_qubits):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(num_qubits)
    
    prog = pq.QProg()
    prog.insert(pq.X(qubits[0]))
    
    for i in range(1, num_qubits):
        prog.insert(pq.X(qubits[i]))
    
    return prog, qubits
