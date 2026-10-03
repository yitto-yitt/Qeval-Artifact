# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def visualize_bell_states():
    backend = AerSimulator(seed_simulator=12345)

    phi_plus = QuantumCircuit(2, 2)
    phi_plus.h(0)
    phi_plus.cx(0, 1)
    phi_plus.measure([0, 1], [0, 1])

    phi_minus = QuantumCircuit(2, 2)
    phi_minus.h(0)
    phi_minus.cx(0, 1)
    phi_minus.z(0)
    phi_minus.measure([0, 1], [0, 1])

    result = backend.run([phi_plus, phi_minus], shots=8192).result()
    counts_plus = result.get_counts(0)
    counts_minus = result.get_counts(1)

    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())

    prob_plus = {
        "00": counts_plus.get("00", 0) / total_plus,
        "11": counts_plus.get("11", 0) / total_plus,
    }
    prob_minus = {
        "00": counts_minus.get("00", 0) / total_minus,
        "11": counts_minus.get("11", 0) / total_minus,
    }

    return {"phi_plus": prob_plus, "phi_minus": prob_minus}
