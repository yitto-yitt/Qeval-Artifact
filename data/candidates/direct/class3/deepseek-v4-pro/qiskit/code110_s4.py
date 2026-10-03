# EVAL_META: task_id=110, framework=qiskit, class=3
import random
from qiskit.circuit.library import HGate, XGate, YGate, ZGate, SGate, SdgGate


def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    gate_types = [HGate, XGate, YGate, ZGate, SGate, SdgGate]
    circuits = []

    for _ in range(n):
        qc = circuit.copy()
        if num_qubits == 0:
            circuits.append(qc)
            continue

        for _ in range(random.randint(1, 5)):
            qubit_index = random.randrange(num_qubits)
            gate = random.choice(gate_types)()
            qubit = [qc.qubits[qubit_index]]
            qc.append(gate, qubit)
            qc.append(gate.inverse(), qubit)

        circuits.append(qc)

    return circuits
