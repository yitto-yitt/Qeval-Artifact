# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def not_gate(a):
    n = 8
    qc = QuantumCircuit(n, n)
    for i in range(n):
        if (a >> i) & 1:
            qc.x(i)
    qc.x(range(n))
    qc.measure(range(n), range(n))
    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled = pm.run(qc)
    result = backend.run(transpiled, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
