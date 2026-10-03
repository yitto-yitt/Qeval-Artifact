# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit

def send_bits(bitstring):
    qc = QuantumCircuit(2, 2)
    
    # Create shared entanglement (Bell pair) between Alice (q0) and Bob (q1)
    qc.h(0)
    qc.cx(0, 1)
    
    # Alice encodes two classical bits on her qubit (q0) via superdense coding
    # bitstring[0] controls X gate, bitstring[1] controls Z gate
    if bitstring[0] == '1':
        qc.x(0)
    if bitstring[1] == '1':
        qc.z(0)
    
    # Bob performs Bell-basis measurement to decode the two bits
    qc.cx(0, 1)
    qc.h(0)
    
    # Measure both qubits
    qc.measure([0, 1], [0, 1])
    
    return qc
