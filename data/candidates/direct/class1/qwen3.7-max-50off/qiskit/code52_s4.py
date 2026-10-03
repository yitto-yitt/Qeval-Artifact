# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit

def send_bits(bitstring):
    qc = QuantumCircuit(2, 2)
    
    # Create shared entanglement (Bell pair) between Alice (q0) and Bob (q1)
    qc.h(0)
    qc.cx(0, 1)
    
    # Alice encodes two classical bits into her single qubit (superdense coding)
    if bitstring[0] == '1':
        qc.x(0)
    if bitstring[1] == '1':
        qc.z(0)
    
    # Quantum communication: Alice sends her one qubit to Bob
    qc.barrier()
    
    # Bob decodes the two classical bits
    qc.cx(0, 1)
    qc.h(0)
    
    # Measure both qubits to recover the two classical bits
    qc.measure(0, 0)
    qc.measure(1, 1)
    
    return qc
