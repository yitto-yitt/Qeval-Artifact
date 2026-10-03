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
    
    # Get the state vector
    statevector = machine.get_output_state(prog)
    
    machine.finalize()
    
    return statevector
