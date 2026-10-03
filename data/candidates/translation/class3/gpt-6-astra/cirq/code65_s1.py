# EVAL_META: task_id=65, framework=cirq, class=3
import cirq

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    for target in range(n - 1, -1, -1):
        circuit.append(cirq.H(qubits[target]))
        for control in range(target):
            circuit.append(
                cirq.CZPowGate(exponent=1 / 2 ** (target - control)).on(
                    qubits[control], qubits[target]
                )
            )
    for index in range(n // 2):
        circuit.append(cirq.SWAP(qubits[index], qubits[n - index - 1]))
    return circuit
