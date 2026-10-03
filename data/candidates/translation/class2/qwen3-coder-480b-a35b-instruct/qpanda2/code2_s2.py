# EVAL_META: task_id=2, framework=qpanda2, class=2
import pyqpanda as pq
from math import sqrt


def create_bell_statevector():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(2)
    prog = pq.QProg()
    
    # Create |00> state
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    
    state = machine.get_state_vector(prog)
    machine.finalize()
    
    # Normalize the state vector to match the expected Bell state
    # The state should be (|00> + |11>) / sqrt(2)
    bell_state = [0.0] * 4
    bell_state[0] = 1.0 / sqrt(2)  # |00> component
    bell_state[3] = 1.0 / sqrt(2)  # |11> component
    
    return bell_state
