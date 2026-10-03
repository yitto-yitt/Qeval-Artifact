# EVAL_META: task_id=2, framework=qpanda, class=2
import pyqpanda3.core as pq
from math import sqrt


def create_bell_statevector():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    
    # Create Bell state |Φ+⟩ = (|00⟩ + |11⟩) / √2
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    
    statevector = pq.get_state_vector(prog, machine)
    pq.destroy_quantum_machine(machine)
    
    return statevector
