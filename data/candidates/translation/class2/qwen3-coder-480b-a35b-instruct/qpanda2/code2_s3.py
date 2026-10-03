# EVAL_META: task_id=2, framework=qpanda2, class=2
import pyqpanda as pq
from math import sqrt


def create_bell_statevector():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    # Create Bell state |Φ+⟩ = (|00⟩ + |11⟩) / √2
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    
    statevector = machine.get_outputstatevector(prog, qubits)
    machine.finalize()
    
    return statevector
