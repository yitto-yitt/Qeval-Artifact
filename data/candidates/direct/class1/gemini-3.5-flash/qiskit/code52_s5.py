# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit

def send_bits(bitstring: str) -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    
    # Step 1: Prepare the entangled pair (Bell state) shared between Alice and Bob
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()
    
    # Step 2: Alice encodes her 2-bit classical message onto her qubit (q0)
    if bitstring == "01":
        qc.z(0)
    elif bitstring == "10":
        qc.x(0)
    elif bitstring == "11":
        qc.x(0)
        qc.z(0)
    
    qc.barrier()
    
    # Step 3: Bob decodes the message using his qubit (q1) and Alice's qubit (q0)
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()
    
    # Step 4: Bob measures both qubits to retrieve the classical bits
    qc.measure(0, 0)
    qc.measure(1, 1)
    
    return qc
