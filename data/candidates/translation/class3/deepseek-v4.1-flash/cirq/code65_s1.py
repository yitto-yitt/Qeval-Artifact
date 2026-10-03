# EVAL_META: task_id=65, framework=cirq, class=3
import cirq

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()

    def swap_registers(n):
        for qubit in range(n // 2):
            circuit.append(cirq.SWAP(qubits[qubit], qubits[n - qubit - 1]))

    def qft_rotations(n):
        if n == 0:
            return
        n -= 1
        circuit.append(cirq.H(qubits[n]))
        for qubit in range(n):
            circuit.append(
                cirq.CZPowGate(exponent=1 / 2 ** (n - qubit)).on(
                    qubits[qubit], qubits[n]
                )
            )
        qft_rotations(n)

    qft_rotations(n)
    swap_registers(n)
    return circuit
