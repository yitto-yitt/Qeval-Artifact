# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def or_gate(a, b):
    # Registers: 3 for a, 3 for b, 3 for output (9 qubits total)
    qr = QuantumRegister(9, 'q')
    cr = ClassicalRegister(3, 'c')
    circuit = QuantumCircuit(qr, cr)

    # Encode integer a on qubits 0,1,2 (bit0 = LSB on qubit 0)
    for i in range(3):
        if (a >> i) & 1:
            circuit.x(qr[i])

    # Encode integer b on qubits 3,4,5
    for i in range(3):
        if (b >> i) & 1:
            circuit.x(qr[3 + i])

    # Compute bitwise OR onto output qubits 6,7,8
    # out = NOT( NOT a AND NOT b )
    for i in range(3):
        circuit.x(qr[i])                      # flip a_i
        circuit.x(qr[3 + i])                  # flip b_i
        circuit.ccx(qr[i], qr[3 + i], qr[6 + i])  # if both flipped → toggle out
        circuit.x(qr[i])                      # restore a_i
        circuit.x(qr[3 + i])                  # restore b_i
        circuit.x(qr[6 + i])                  # final NOT to get OR

    # Measure output qubits to classical bits
    # qubit6 (LSB) -> cr[0], qubit7 -> cr[1], qubit8 (MSB) -> cr[2]
    for i in range(3):
        circuit.measure(qr[6 + i], cr[i])

    # Simulate
    backend = AerSimulator()
    job = backend.run(circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()

    # Build full probability distribution over all 3-bit strings
    distribution = {}
    for val in range(8):
        bitstr = f"{val:03b}"
        distribution[bitstr] = 0.0

    total = sum(counts.values())
    for bitstr, cnt in counts.items():
        distribution[bitstr] = cnt / total

    return distribution
