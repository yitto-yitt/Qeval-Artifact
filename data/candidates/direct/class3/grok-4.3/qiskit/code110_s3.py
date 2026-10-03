# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, random_clifford

def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    target = Clifford(circuit)
    result = []
    for _ in range(n):
        rc = random_clifford(num_qubits)
        rc_circ = rc.to_circuit()
        comp = target.compose(rc.adjoint())
        comp_circ = comp.to_circuit()
        new_circ = rc_circ.compose(comp_circ)
        result.append(new_circ)
    return result
