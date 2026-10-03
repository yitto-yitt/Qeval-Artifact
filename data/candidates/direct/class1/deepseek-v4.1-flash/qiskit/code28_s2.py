# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def visualize_bell_states():
    simulator = AerSimulator()

    def _bell_circuit(minus):
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        if minus:
            qc.z(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])
        return qc

    results = {}
    for name, minus in (("phi_plus", False), ("phi_minus", True)):
        circuit = _bell_circuit(minus)
        compiled = transpile(circuit, simulator)
        counts = simulator.run(compiled, shots=8192).result().get_counts()
        total = sum(counts.values())
        results[name] = {bitstring: count / total for bitstring, count in counts.items()}

    return results
