# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit

def send_bits(bitstring: str) -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    
    # Share entanglement
    qc.h(0)
    qc.cnot(0, 1)
    qc.barrier()
    
    # Alice encodes
    if bitstring[0] == '1':
        qc.x(0)
    if bitstring[1] == '1':
        qc.z(0)
    qc.barrier()
    
    # Bob decodes
    qc.cnot(0, 1)
    qc.h(0)
    qc.barrier()
    
    # Measure
    qc.measure(0, 0)
    qc.measure(1, 1)
    
    return qc
