# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


def or_gate(a, b):
    qr_a = QuantumRegister(3, 'a')
    qr_b = QuantumRegister(3, 'b')
    qr_out = QuantumRegister(3, 'out')
    cr = ClassicalRegister(3, 'c')

    qc = QuantumCircuit(qr_a, qr_b, qr_out, cr)

    # Initialize a qubits to represent integer a
    for i in range(3):
        if (a >> i) & 1:
            qc.x(qr_a[i])

    # Initialize b qubits to represent integer b
    for i in range(3):
        if (b >> i) & 1:
            qc.x(qr_b[i])

    # Compute bitwise OR for each bit position
    # out = a OR b = a XOR b XOR (a AND b)
    # Step 1: CNOT a -> out  (out = a)
    # Step 2: CNOT b -> out  (out = a XOR b)
    # Step 3: Toffoli a,b -> out (out = a XOR b XOR (a AND b) = a OR b)
    for i in range(3):
        qc.cx(qr_a[i], qr_out[i])
        qc.cx(qr_b[i], qr_out[i])
        qc.ccx(qr_a[i], qr_b[i], qr_out[i])

    # Measure output qubits
    for i in range(3):
        qc.measure(qr_out[i], cr[i])

    # Simulate the circuit
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Convert counts to probability distribution
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
