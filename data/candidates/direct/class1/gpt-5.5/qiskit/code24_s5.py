# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def dj_algorithm(oracle):
    total_qubits = oracle.num_qubits
    input_qubits = total_qubits - 1

    circuit = QuantumCircuit(total_qubits)
    circuit.x(input_qubits)
    circuit.h(range(total_qubits))

    if isinstance(oracle, QuantumCircuit):
        circuit.compose(oracle, qubits=range(total_qubits), inplace=True)
    else:
        circuit.append(oracle, range(total_qubits))

    circuit.h(range(input_qubits))

    state = Statevector.from_instruction(circuit)
    probs = state.probabilities_dict(qargs=list(range(input_qubits)))

    return {format(i, f"0{input_qubits}b"): float(probs.get(format(i, f"0{input_qubits}b"), 0.0)) for i in range(2 ** input_qubits)}
