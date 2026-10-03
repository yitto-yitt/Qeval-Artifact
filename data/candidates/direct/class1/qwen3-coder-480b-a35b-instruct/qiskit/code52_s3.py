# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def send_bits(bitstring):
    """
    Implements superdense coding to transmit two classical bits using one qubit,
    assuming the sender and receiver already share an entangled pair (Bell state).

    Args:
        bitstring (str): A string of two classical bits ('00', '01', '10', or '11')

    Returns:
        QuantumCircuit: The quantum circuit implementing the superdense coding protocol
    """
    # Create quantum registers: 2 qubits (one for Alice's operations, one for Bob's reception)
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    
    qc = QuantumCircuit(qr, cr)
    
    # We assume Alice and Bob initially share the Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
    # This means qubit 0 is with Alice and qubit 1 is with Bob
    
    # Encode the two classical bits according to superdense coding protocol:
    if bitstring == '11':
        # Apply X gate followed by Z gate to encode '11'
        qc.x(qr[0])
        qc.z(qr[0])
    elif bitstring == '10':
        # Apply X gate to encode '10'
        qc.x(qr[0])
    elif bitstring == '01':
        # Apply Z gate to encode '01'
        qc.z(qr[0])
    # For '00', do nothing - identity operation
    
    # At this point, Alice sends her qubit (qr[0]) to Bob
    # Bob now has both qubits and can decode the message by applying the inverse of
    # the Bell preparation circuit
    
    # Apply CNOT with Alice's qubit as control and Bob's qubit as target
    qc.cx(qr[0], qr[1])
    
    # Apply Hadamard on Alice's qubit
    qc.h(qr[0])
    
    # Measure both qubits to reveal the transmitted classical bits
    qc.measure(qr[0], cr[0])
    qc.measure(qr[1], cr[1])
    
    return qc
