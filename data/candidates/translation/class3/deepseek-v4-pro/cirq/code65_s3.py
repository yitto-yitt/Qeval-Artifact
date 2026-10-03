# EVAL_META: task_id=65, framework=cirq, class=3
import cirq

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    def swap_registers():
        for i in range(n // 2):
            circuit.append(cirq.SWAP(qubits[i], qubits[n - i - 1]))

    def qft_rotations(m):
        if m == 0:
            return
        m -= 1
        circuit.append(cirq.H(qubits[m]))
        for q in range(m):
            circuit.append(
                cirq.CZPowGate(exponent=1 / (2 ** (m - q))).on(
                    qubits[q], qubits[m]
                )
            )
        qft_rotations(m)

    qft_rotations(n)
    swap_registers()
    return circuit
