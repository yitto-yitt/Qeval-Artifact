# EVAL_META: task_id=52, framework=qiskit, class=1

from qiskit import QuantumCircuit

def send_bits(bitstring: str) -> QuantumCircuit:
    """
    Provide a quantum circuit for transmitting two classical bits through one
    qubit of quantum communication when sender and receiver share entanglement.
    """
    qc = QuantumCircuit(2, 2)
    
    # Step 1: Create entangled pair (shared between Alice and Bob)
    qc.h(0)
    qc.cnot(0, 1)
    
    # Step 2: Alice encodes her bits on her qubit (qubit 0)
    if bitstring[0] == '1':
        qc.x(0)
    if bitstring[1] == '1':
        qc.z(0)
        
    # Step 3: Bob decodes the transmission using both qubits
    qc.cnot(0, 1)
    qc.h(0)
    
    # Step 4: Bob measures both qubits to retrieve the two classical bits
    qc.measure([0, 1], [0, 1])
    
    return qc
