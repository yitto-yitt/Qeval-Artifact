# EVAL_META: task_id=67, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

def chsh_circuit(alice, bob):
    # Create quantum and classical registers
    qr = QuantumRegister(2)
    cr = ClassicalRegister(2)
    qc = QuantumCircuit(qr, cr)
    
    # Prepare entangled state (Bell state)
    qc.h(0)
    qc.cx(0, 1)
    
    # Alice's measurement settings
    if alice == 1:
        qc.ry(2 * 0.7853981633974483, 0)  # Rotate by pi/4
    
    # Bob's measurement settings
    if bob == 0:
        qc.ry(-0.7853981633974483, 1)   # Rotate by -pi/4
    else:
        qc.ry(-3 * 0.7853981633974483, 1)  # Rotate by -3pi/4
    
    # Measure both qubits
    qc.measure(0, 0)
    qc.measure(1, 1)
    
    return qc
