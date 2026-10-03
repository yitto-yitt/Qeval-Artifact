# EVAL_META: task_id=52, framework=qiskit, class=1

from qiskit import QuantumCircuit

def send_bits(bitstring: str) -> QuantumCircuit:
    """
    Provide a quantum circuit for transmitting two classical bits through 
    one qubit of quantum communication when sender and receiver share entanglement.
    """
    qc = QuantumCircuit(2, 2)
    
    # Step 1: Share entanglement (Bell state preparation)
    qc.h(0)
    qc.cx(0, 1)
    
    # Step 2: Sender (Alice) encodes the 2-bit string on her qubit (q0)
    if bitstring[0] == '1':
        qc.x(0)
    if bitstring[1] == '1':
        qc.z(0)
        
    # Step 3: Receiver (Bob) decodes the message
    qc.cx(0, 1)
    qc.h(0)
    
    # Step 4: Measurement
    qc.measure([0, 1], [0, 1])
    
    return qc
