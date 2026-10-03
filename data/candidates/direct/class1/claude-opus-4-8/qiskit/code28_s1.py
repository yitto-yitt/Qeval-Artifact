# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def visualize_bell_states():
    simulator = AerSimulator()
    shots = 4096
    result = {}

    for name, minus in [('phi_plus', False), ('phi_minus', True)]:
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        if minus:
            qc.z(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        counts = simulator.run(qc, shots=shots).result().get_counts()
        dist = {k: v / shots for k, v in counts.items()}
        result[name] = dist

    return result
