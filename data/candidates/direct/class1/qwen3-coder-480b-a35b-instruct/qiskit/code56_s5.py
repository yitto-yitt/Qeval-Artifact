# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator


def not_gate(a):
    # Create quantum registers
    qr = QuantumRegister(8)
    cr = ClassicalRegister(8)
    qc = QuantumCircuit(qr, cr)

    # Initialize the input bits based on 'a'
    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)

    # Apply NOT gates to all qubits
    for i in range(8):
        qc.x(i)

    # Measure all qubits
    qc.measure(qr, cr)

    # Simulate the circuit
    simulator = AerSimulator()
    result = simulator.run(qc).result()
    counts = result.get_counts()

    # Convert counts to probabilities
    total_shots = sum(counts.values())
    prob_dist = {state: count / total_shots for state, count in counts.items()}

    return prob_dist
