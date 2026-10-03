# EVAL_META: task_id=84, framework=cirq, class=3
import cirq
import numpy as np

class CustomU3(cirq.Gate):
    def __init__(self, theta, phi, lam):
        self.theta = theta
        self.phi = phi
        self.lam = lam

    def _num_qubits_(self) -> int:
        return 1

    def _unitary_(self) -> np.ndarray:
        cos_t = np.cos(self.theta / 2)
        sin_t = np.sin(self.theta / 2)
        return np.array([
            [cos_t, -np.exp(1j * self.lam) * sin_t],
            [np.exp(1j * self.phi) * sin_t, np.exp(1j * (self.phi + self.lam)) * cos_t]
        ], dtype=np.complex128)

    def _circuit_diagram_info_(self, args):
        return f"U3({self.theta},{self.phi},{self.lam})"

def controlled_custom_unitary_circuit():
    qubits = cirq.LineQubit.range(2)
    custom_gate = CustomU3(0.3, 0.2, 0.1)
    controlled_gate = custom_gate.controlled()
    
    circuit = cirq.Circuit()
    circuit.append(controlled_gate(qubits[0], qubits[1]))
    return circuit
