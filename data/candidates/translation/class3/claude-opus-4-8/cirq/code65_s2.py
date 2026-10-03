# EVAL_META: task_id=65, framework=cirq, class=3
import cirq
from numpy import pi

def QFT(n):
    qubits = [cirq.LineQubit(i) for i in range(n)]
    circuit = cirq.Circuit()

    def qft_rotations(circuit, m):
        if m == 0:
            return circuit
        m -= 1
        circuit.append(cirq.H(qubits[m]))
        for qubit in range(m):
            circuit.append(cirq.CZPowGate(exponent=1/2**(m-qubit)).on(qubits[qubit], qubits[m]))
        qft_rotations(circuit, m)

    def swap_registers(circuit, m):
        for qubit in range(m//2):
            circuit.append(cirq.SWAP(qubits[qubit], qubits[m-qubit-1]))
        return circuit

    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
