# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit.quantum_info import random_clifford, Clifford

def equivalent_clifford_circuit(circuit, n):
    if isinstance(circuit, Clifford):
        base = circuit.to_circuit()
    else:
        base = circuit.copy()
    num_qubits = base.num_qubits
    result = []
    for _ in range(n):
        qc = base.copy()
        r = random_clifford(num_qubits)
        rc = r.to_circuit()
        inv = r.adjoint().to_circuit()
        qc = qc.compose(rc)
        qc = qc.compose(inv)
        result.append(qc)
    return result
