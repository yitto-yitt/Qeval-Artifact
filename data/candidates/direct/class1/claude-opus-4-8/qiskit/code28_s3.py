# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def visualize_bell_states():
    simulator = AerSimulator()
    result = {}

    for name in ('phi_plus', 'phi_minus'):
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        if name == 'phi_minus':
            qc.z(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])

        shots = 4096
        counts = simulator.run(qc, shots=shots).result().get_counts()
        dist = {bitstring: count / shots for bitstring, count in counts.items()}
        result[name] = dist

    return result
