# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def not_gate(a):
    qc = QuantumCircuit(8, 8)
    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)
    for i in range(8):
        qc.x(i)
    qc.measure(range(8), range(8))
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit, shots=1024).result()
    counts = result.get_counts(qc)
    total = sum(counts.values())
    return {state: count / total for state, count in counts.items()}
