# EVAL_META: task_id=65, framework=cirq, class=3
import cirq
from numpy import pi

def QFT(n):
    qubits = [cirq.LineQubit(i) for i in range(n)]
    circuit = cirq.Circuit()

    def qft_rotations(m):
        if m == 0:
            return
        m -= 1
        circuit.append(cirq.H(qubits[m]))
        for qubit in range(m):
            angle = pi / 2**(m - qubit)
            circuit.append(cirq.CZPowGate(exponent=angle / pi).on(qubits[qubit], qubits[m]))
        qft_rotations(m)

    qft_rotations(n)
    for qubit in range(n // 2):
        circuit.append(cirq.SWAP(qubits[qubit], qubits[n - qubit - 1]))
    return circuit
