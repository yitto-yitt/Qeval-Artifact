# EVAL_META: task_id=5, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    # Prepare state "01" - qubit 0 should be |0>, qubit 1 should be |1>
    # By default qubits are in |0> state, so we just need to flip qubit 1
    prog << pq.X(qubits[1])
    
    machine.finalize()
    return prog
