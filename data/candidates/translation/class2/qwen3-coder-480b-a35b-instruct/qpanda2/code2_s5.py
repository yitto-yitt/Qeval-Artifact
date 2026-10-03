# EVAL_META: task_id=2, framework=qpanda2, class=2
import pyqpanda as pq
from math import sqrt


def create_bell_statevector():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(2)
    prog = pq.QProg()
    
    # Create |00> + |11> state (Phi+ Bell state)
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    
    state = machine.get_state_vector(prog, qubits)
    machine.destroy_qvm()
    
    # Normalize the state vector to match the expected Bell state
    # The state vector should represent (|00> + |11>) / sqrt(2)
    normalized_state = state / sqrt(2)
    
    return normalized_state
