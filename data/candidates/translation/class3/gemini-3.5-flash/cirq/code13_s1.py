# EVAL_META: task_id=13, framework=cirq, class=3
import cirq
import numpy as np

class CustomUGate(cirq.Gate):
    def __init__(self, theta, phi, lmda):
        super().__init__()
        self.theta = theta
        self.phi = phi
        self.lmda = lmda

    def _num_qubits_(self) -> int:
        return 1

    def _unitary_(self) -> np.ndarray:
        theta, phi, lmda = self.theta, self.phi, self.lmda
        cos = np.cos(theta / 2)
        sin = np.sin(theta / 2)
        return np.array([
            [cos, -np.exp(1j * lmda) * sin],
            [np.exp(1j * phi) * sin, np.exp(1j * (phi + lmda)) * cos]
        ], dtype=np.complex128)

    def _circuit_diagram_info_(self, args) -> str:
        return f"U({self.theta},{self.phi},{self.lmda})"

def custom_rotation_gate():
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    gate = CustomUGate(np.pi / 2, np.pi / 2, np.pi / 2)
    circuit.append(gate(qubit))
    return circuit
