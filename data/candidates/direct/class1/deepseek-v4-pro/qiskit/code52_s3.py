# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit

def send_bits(bitstring):
    qc = QuantumCircuit(2, 2)
    
    # Create entangled Bell pair between sender (q0) and receiver (q1)
    qc.h(0)
    qc.cx(0, 1)
    
    # Sender encodes two classical bits on their qubit
    if bitstring[0] == '1':
        qc.z(0)
    if bitstring[1] == '1':
        qc.x(0)
    
    # Receiver decodes the information
    qc.cx(0, 1)
    qc.h(0)
    
    # Measure both qubits to recover the classical bits
    qc.measure([0, 1], [0, 1])
    
    return qc
