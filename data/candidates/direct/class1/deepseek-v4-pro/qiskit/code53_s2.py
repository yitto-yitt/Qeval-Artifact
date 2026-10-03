# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    xor_val = a ^ b

    qc = QuantumCircuit(8, 8)

    for i in range(8):
        if (xor_val >> i) & 1:
            qc.x(i)

    qc.measure(range(8), range(8))

    simulator = AerSimulator()
    job = simulator.run(qc, shots=1024)
    counts = job.result().get_counts(qc)

    total_shots = sum(counts.values())
    return {state: count / total_shots for state, count in counts.items()}
