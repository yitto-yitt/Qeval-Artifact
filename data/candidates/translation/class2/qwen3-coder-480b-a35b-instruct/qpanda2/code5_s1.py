# EVAL_META: task_id=5, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    # Prepare the state "01" - which means qubit 0 should be |1> and qubit 1 should be |0>
    prog << pq.X(qubits[0])  # Apply X gate to first qubit to make it |1>
    
    return prog
