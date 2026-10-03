# EVAL_META: task_id=65, framework=cirq, class=3
import cirq
from numpy import pi

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    def qft_rotations(circuit, num_qubits):
        if num_qubits == 0:
            return circuit
        num_qubits -= 1
        circuit.append(cirq.H(qubits[num_qubits]))
        for qubit in range(num_qubits):
            angle = pi / (2 ** (num_qubits - qubit))
            circuit.append(cirq.CZPowGate(exponent=angle / pi).on(qubits[qubit], qubits[num_qubits]))
        qft_rotations(circuit, num_qubits)

    qft_rotations(circuit, n)
    for qubit in range(n // 2):
        circuit.append(cirq.SWAP(qubits[qubit], qubits[n - qubit - 1]))
    return circuit
