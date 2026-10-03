# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit

def send_bits(bitstring):
    qc = QuantumCircuit(2)  # qubit 0 Alice, qubit 1 Bob, they share a Bell pair
    # Encode the two bits onto Alice's qubit using Pauli operators
    if bitstring == '00':
        pass  # identity
    elif bitstring == '01':
        qc.x(0)
    elif bitstring == '10':
        qc.z(0)
    elif bitstring == '11':
        qc.x(0)
        qc.z(0)
    else:
        raise ValueError("bitstring must be a two-bit string like '00', '01', '10', '11'")
    return qc
