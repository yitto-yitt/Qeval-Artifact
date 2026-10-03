# EVAL_META: task_id=5, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    # To prepare state "01", we need to apply X gate to the first qubit (q[0])
    # since initial state is |00>, applying X to first qubit gives |01>
    prog << pq.X(qubits[1])  # Apply X to second qubit (index 1) to get |01>
    
    machine.finalize()
    return prog, qubits, machine
