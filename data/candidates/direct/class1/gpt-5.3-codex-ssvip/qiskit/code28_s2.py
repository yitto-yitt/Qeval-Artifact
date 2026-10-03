# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def visualize_bell_states():
    simulator = AerSimulator()
    shots = 4096

    circuits = {}

    qc_plus = QuantumCircuit(2, 2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    qc_plus.measure([0, 1], [0, 1])
    circuits["phi_plus"] = qc_plus

    qc_minus = QuantumCircuit(2, 2)
    qc_minus.h(0)
    qc_minus.z(0)
    qc_minus.cx(0, 1)
    qc_minus.measure([0, 1], [0, 1])
    circuits["phi_minus"] = qc_minus

    result = simulator.run(list(circuits.values()), shots=shots).result()

    output = {}
    for name, qc in circuits.items():
        counts = result.get_counts(qc)
        probs = {bitstring: count / shots for bitstring, count in counts.items()}
        output[name] = probs

    return output
