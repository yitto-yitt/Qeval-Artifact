# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def send_bits(bitstring):
    """
    Implements superdense coding to transmit two classical bits using one qubit,
    assuming the sender and receiver already share an entangled pair (Bell state).

    Args:
        bitstring (str): A string of two bits ('00', '01', '10', or '11') to be transmitted

    Returns:
        QuantumCircuit: A quantum circuit implementing the superdense coding protocol
    """
    # Create quantum registers
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)

    # Assume Alice has qubit 0 and Bob has qubit 1, and they share |Φ+⟩ = (|00⟩ + |11⟩)/√2
    # This is typically prepared beforehand, so we'll apply the encoding operations
    
    # Encoding based on the two-bit message
    if bitstring == '11':
        qc.x(qr[0])  # Apply X gate for bit '1' in the second position
        qc.z(qr[0])  # Apply Z gate for bit '1' in the first position
    elif bitstring == '10':
        qc.x(qr[0])  # Apply X gate for bit '1' in the second position
    elif bitstring == '01':
        qc.z(qr[0])  # Apply Z gate for bit '1' in the first position
    # For '00', do nothing - identity operation

    # Now Alice sends her qubit (qubit 0) to Bob
    # Bob performs Bell measurement on both qubits
    qc.cx(qr[0], qr[1])
    qc.h(qr[0])
    qc.measure(qr[0], cr[0])
    qc.measure(qr[1], cr[1])

    return qc
