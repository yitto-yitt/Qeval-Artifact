# EVAL_META: task_id=52, framework=qiskit, class=1

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

def send_bits(bitstring):
    # Create quantum registers
    q = QuantumRegister(2, 'q')
    c = ClassicalRegister(2, 'c')
    
    # Create the circuit
    qc = QuantumCircuit(q, c)
    
    # Prepare Bell state (entanglement): |Φ+⟩ = (|00⟩ + |11⟩)/√2
    qc.h(q[0])
    qc.cx(q[0], q[1])
    
    # Encode the two classical bits
    # bitstring is expected to be a 2-bit string like "00", "01", "10", or "11"
    if bitstring[0] == '1':
        qc.z(q[0])  # Apply Z gate for first bit
    if bitstring[1] == '1':
        qc.x(q[0])  # Apply X gate for second bit
    
    # Perform Bell measurement
    qc.cx(q[0], q[1])
    qc.h(q[0])
    
    # Measure both qubits
    qc.measure(q[0], c[0])
    qc.measure(q[1], c[1])
    
    return qc
