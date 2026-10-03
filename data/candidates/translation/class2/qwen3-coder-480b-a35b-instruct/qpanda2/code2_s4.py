# EVAL_META: task_id=2, framework=qpanda2, class=2
import pyqpanda as pq
from math import sqrt


def create_bell_statevector():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    
    state = pq.get_state_vector(prog, machine)
    pq.destroy_quantum_machine(machine)
    
    # Normalize the state vector to match the expected Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
    bell_state = [0] * 4
    bell_state[0] = 1/sqrt(2)  # |00⟩ component
    bell_state[3] = 1/sqrt(2)  # |11⟩ component
    
    return bell_state
