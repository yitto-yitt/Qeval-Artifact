# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford
import random

def equivalent_clifford_circuit(circuit, n):
    base = Clifford(circuit)
    num_qubits = circuit.num_qubits
    results = []

    for _ in range(n):
        qc = QuantumCircuit(num_qubits, num_qubits if circuit.num_clbits > 0 else 0)

        depth = random.randint(max(1, num_qubits), max(2, 4 * num_qubits))
        one_q_gates = ["h", "s", "sdg", "x", "y", "z"]
        two_q_gates = ["cx", "cz", "swap"]

        for _ in range(depth):
            if num_qubits == 1 or random.random() < 0.7:
                q = random.randrange(num_qubits)
                g = random.choice(one_q_gates)
                getattr(qc, g)(q)
            else:
                q1, q2 = random.sample(range(num_qubits), 2)
                g = random.choice(two_q_gates)
                getattr(qc, g)(q1, q2)

        delta = Clifford(qc).adjoint().compose(base)
        delta_circ = delta.to_circuit()
        eq = qc.compose(delta_circ)

        if circuit.num_clbits > 0:
            for inst, qargs, cargs in circuit.data:
                if inst.name == "measure":
                    eq.measure(qargs[0]._index, cargs[0]._index)

        results.append(eq)

    return results
