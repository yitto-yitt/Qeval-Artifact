# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit


def send_bits(bitstring):
    """
    Implements superdense coding to transmit two classical bits using one qubit of quantum communication
    when sender and receiver share entanglement.

    Args:
        bitstring (str): A string of two bits ('00', '01', '10', or '11') to be transmitted

    Returns:
        QuantumCircuit: A quantum circuit implementing the superdense coding protocol
    """
    # Create a quantum circuit with 2 qubits and 2 classical bits
    qc = QuantumCircuit(2, 2)

    # Step 1: Create entangled pair (shared entanglement between sender and receiver)
    # Apply Hadamard gate to first qubit
    qc.h(0)
    # Apply CNOT gate with first qubit as control and second as target
    qc.cx(0, 1)

    # At this point, we have a Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
    # Qubit 0 is with the sender, qubit 1 is with the receiver

    # Step 2: Encode the two-bit message on the sender's qubit (qubit 0)
    if bitstring == '11':
        # For '11': Apply both X and Z gates
        qc.x(0)
        qc.z(0)
    elif bitstring == '10':
        # For '10': Apply only X gate
        qc.x(0)
    elif bitstring == '01':
        # For '01': Apply only Z gate
        qc.z(0)
    # For '00': Apply no gates (identity operation)

    # Step 3: Send the encoded qubit (qubit 0) to the receiver
    # This step is conceptual - in the circuit, we just continue with operations

    # Step 4: Decoding at the receiver's end
    # Apply CNOT with qubit 0 as control and qubit 1 as target
    qc.cx(0, 1)
    # Apply Hadamard on qubit 0
    qc.h(0)

    # Step 5: Measure both qubits to retrieve the original two bits
    qc.measure([0, 1], [0, 1])

    return qc
