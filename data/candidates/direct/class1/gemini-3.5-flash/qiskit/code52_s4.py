# EVAL_META: task_id=52, framework=qiskit, class=1

from qiskit import QuantumCircuit

def send_bits(bitstring: str) -> QuantumCircuit:
    """
    Provide a quantum circuit for transmitting two classical bits through one qubit 
    of quantum communication when sender and receiver share entanglement.
    """
    qc = QuantumCircuit(2, 2)
    
    # 1. Prepare entangled pair (Bell state) shared between Alice (q1) and Bob (q0)
    qc.h(1)
    qc.cx(1, 0)
    
    # 2. Alice encodes the classical bits into her qubit (q1)
    if bitstring[1] == '1':
        qc.x(1)
    if bitstring[0] == '1':
        qc.z(1)
        
    # 3. Bob decodes the message using both qubits
    qc.cx(1, 0)
    qc.h(1)
    
    # 4. Bob measures the qubits to retrieve the two classical bits
    qc.measure([0, 1], [0, 1])
    
    return qc
