# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import itertools

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()

    # First rotation layer: Ry(θ) and Rz(θ) on all qubits
    for i, q in enumerate(qubits):
        circuit += cirq.ry(cirq.ParameterVar(f"Ry_0_{i}")).on(q)
        circuit += cirq.rz(cirq.ParameterVar(f"Rz_0_{i}")).on(q)

    # First entanglement layer: linear CNOTs
    for i in range(len(qubits) - 1):
        circuit += cirq.CNOT(qubits[i], qubits[i + 1])

    # Barrier
    circuit += cirq.Moment()

    # Second rotation layer
    for i, q in enumerate(qubits):
        circuit += cirq.ry(cirq.ParameterVar(f"Ry_1_{i}")).on(q)
        circuit += cirq.rz(cirq.ParameterVar(f"Rz_1_{i}")).on(q)

    # Second entanglement layer
    for i in range(len(qubits) - 1):
        circuit += cirq.CNOT(qubits[i], qubits[i + 1])

    # Barrier
    circuit += cirq.Moment()

    return circuit
