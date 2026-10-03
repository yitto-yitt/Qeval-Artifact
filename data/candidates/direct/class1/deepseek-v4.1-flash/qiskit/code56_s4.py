# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def not_gate(a):
    if not (0 <= a <= 255):
        raise ValueError("a must be an 8-bit integer in [0, 255]")

    qr = QuantumRegister(8, 'q')
    cr = ClassicalRegister(8, 'c')
    qc = QuantumCircuit(qr, cr)

    bits = format(a, '08b')
    for i, bit in enumerate(reversed(bits)):
        if bit == '1':
            qc.x(qr[i])

    qc.x(qr)
    qc.measure(qr, cr)

    backend = AerSimulator()
    shots = 1024
    result = backend.run(qc, shots=shots).result()
    counts = result.get_counts(qc)
    return {state: count / shots for state, count in counts.items()}
