# EVAL_META: task_id=6, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_state_prep(num_qubits):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(num_qubits)
    
    prog = pq.QProg()
    # Apply X gate to first qubit to prepare |1> state
    prog.insert(pq.X(qubits[0]))
    
    # For multi-qubit case, we need to tensor with |0>^(n-1) state
    # But since default initialization is |0>, we only need to flip the first qubit
    
    return prog
