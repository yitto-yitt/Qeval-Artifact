# EVAL_META: task_id=110, framework=qiskit, class=3
import random

from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, SGate, XGate, YGate, ZGate, CXGate, CZGate, SwapGate


def _random_clifford_gate(num_qubits, rng):
    one_qubit_gates = [HGate, SGate, XGate, YGate, ZGate]
    two_qubit_gates = [CXGate, CZGate, SwapGate]

    if num_qubits < 2:
        available = one_qubit_gates
    else:
        available = one_qubit_gates + two_qubit_gates

    gate_cls = rng.choice(available)
    gate = gate_cls()

    if gate.num_qubits == 1:
        qargs = [rng.randrange(num_qubits)]
    else:
        first = rng.randrange(num_qubits)
        second = rng.randrange(num_qubits - 1)
        if second >= first:
            second += 1
        qargs = [first, second]

    return gate, qargs


def equivalent_clifford_circuit(circuit, n):
    """Return n random Clifford circuits equivalent to the input circuit."""
    outputs = []
    rng = random.Random()

    for _ in range(n):
        qc = circuit.copy()
        num_qubits = qc.num_qubits

        identity_blocks = []
        num_blocks = rng.randint(1, 4)

        for _ in range(num_blocks):
            gate, qubit_indices = _random_clifford_gate(num_qubits, rng)
            qubits = [qc.qubits[idx] for idx in qubit_indices]
            qc.append(gate, qubits)
            identity_blocks.append((gate, qubits))

        for gate, qubits in reversed(identity_blocks):
            qc.append(gate.inverse(), qubits)

        outputs.append(qc)

    return outputs
