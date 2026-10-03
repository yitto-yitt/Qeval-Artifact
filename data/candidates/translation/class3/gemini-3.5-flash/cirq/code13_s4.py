# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

class CustomRotationGate(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def _unitary_(self) -> np.ndarray:
        return np.array([
            [1/np.sqrt(2), -1j/np.sqrt(2)],
            [1j/np.sqrt(2), -1/np.sqrt(2)]
        ], dtype=np.complex128)

    def _circuit_diagram_info_(self, args) -> str:
        return "U"

def custom_rotation_gate():
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    circuit.append(CustomRotationGate()(qubit))
    return circuit
