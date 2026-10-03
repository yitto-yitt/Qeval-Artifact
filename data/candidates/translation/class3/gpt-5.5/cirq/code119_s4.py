# EVAL_META: task_id=119, framework=cirq, class=3
import cirq
import numpy as np


class _CDKMRippleCarryAdderGate(cirq.Gate):
    def __init__(self, num_state_qubits, kind):
        self.num_state_qubits = int(num_state_qubits)
        self.kind = kind
        if self.num_state_qubits < 1:
            raise ValueError("num_state_qubits must be at least 1")
        if self.kind not in ("full", "half", "fixed"):
            raise ValueError("kind must be 'full', 'half', or 'fixed'")

    def _num_qubits_(self):
        n = self.num_state_qubits
        if self.kind == "full":
            return 2 * n + 2
        if self.kind == "half":
            return 2 * n + 2
        return 2 * n + 1

    def _unitary_(self):
        n = self.num_state_qubits
        m = self._num_qubits_()
        dim = 1 << m
        mat = np.zeros((dim, dim), dtype=complex)

        for x in range(dim):
            bits = [(x >> i) & 1 for i in range(m)]

            if self.kind == "full":
                cin = bits[0]
                a_start = 1
                b_start = 1 + n
                cout_idx = 1 + 2 * n
                a = sum(bits[a_start + i] << i for i in range(n))
                b = sum(bits[b_start + i] << i for i in range(n))
                total = a + b + cin
                b_new = total & ((1 << n) - 1)
                cout_new = (total >> n) & 1
                out = bits[:]
                for i in range(n):
                    out[b_start + i] = (b_new >> i) & 1
                out[cout_idx] ^= cout_new

            elif self.kind == "half":
                a_start = 0
                b_start = n
                cout_idx = 2 * n
                help_idx = 2 * n + 1
                cin = bits[help_idx]
                a = sum(bits[a_start + i] << i for i in range(n))
                b = sum(bits[b_start + i] << i for i in range(n))
                total = a + b + cin
                b_new = total & ((1 << n) - 1)
                cout_new = (total >> n) & 1
                out = bits[:]
                for i in range(n):
                    out[b_start + i] = (b_new >> i) & 1
                out[cout_idx] ^= cout_new

            else:
                a_start = 0
                b_start = n
                help_idx = 2 * n
                cin = bits[help_idx]
                a = sum(bits[a_start + i] << i for i in range(n))
                b = sum(bits[b_start + i] << i for i in range(n))
                total = a + b + cin
                b_new = total & ((1 << n) - 1)
                out = bits[:]
                for i in range(n):
                    out[b_start + i] = (b_new >> i) & 1

            y = sum(bit << i for i, bit in enumerate(out))
            mat[y, x] = 1.0

        return mat

    def _circuit_diagram_info_(self, args):
        return [f"CDKM({self.kind},{self.num_state_qubits})"] * self._num_qubits_()


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    gate = _CDKMRippleCarryAdderGate(num_state_qubits, kind)
    qubits = cirq.LineQubit.range(cirq.num_qubits(gate))
    return cirq.Circuit(gate.on(*qubits))
