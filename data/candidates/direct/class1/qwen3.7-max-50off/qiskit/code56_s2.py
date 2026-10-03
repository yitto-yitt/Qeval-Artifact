# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    a_bin = format(a & 0xFF, '08b')

    qc = QuantumCircuit(8, 8)

    # Initialize qubits to represent input 'a'
    # Qiskit qubit 0 is LSB (rightmost bit of binary string)
    for i in range(8):
        if a_bin[7 - i] == '1':
            qc.x(i)

    # Apply bitwise NOT (X gate to all qubits)
    for i in range(8):
        qc.x(i)

    # Measure all qubits
    qc.measure(range(8), range(8))

    # Simulate
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Convert counts to probability distribution
    total_shots = sum(counts.values())
    prob_dist = {k: v / total_shots for k, v in counts.items()}

    return prob_dist
