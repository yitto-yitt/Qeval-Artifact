# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
import builtins

from pyqpanda import QMachineType, init_quantum_machine, QCircuit, RY, X


def circuit_from_probability_dist(probability_dist):
    if not hasattr(circuit_from_probability_dist, "_qvm"):
        circuit_from_probability_dist._qvm = init_quantum_machine(QMachineType.CPU)

    qvm = circuit_from_probability_dist._qvm

    num_qubits = math.ceil(math.log2(builtins.max(probability_dist.keys()) + 1)) or 1
    qubits = qvm.qAlloc_many(num_qubits)

    amplitudes = []
    for basis_state in range(2 ** num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    def controlled_circuit(circuit, controls):
        wrapped = QCircuit()
        wrapped.insert(circuit)
        try:
            ret = wrapped.control(controls)
            return wrapped if ret is None else ret
        except Exception:
            ret = wrapped.set_control(controls)
            return wrapped if ret is None else ret

    def build_state_circuit(state, qs):
        circuit = QCircuit()
        m = len(qs)
        if m == 0:
            return circuit

        half = 1 << (m - 1)
        left = state[:half]
        right = state[half:]

        norm_left = math.sqrt(builtins.sum(a * a for a in left))
        norm_right = math.sqrt(builtins.sum(a * a for a in right))

        theta = 2.0 * math.atan2(norm_right, norm_left)
        target = qs[m - 1]
        circuit.insert(RY(target, theta))

        if norm_left > 0:
            left_state = [a / norm_left for a in left]
            left_circuit = build_state_circuit(left_state, qs[:m - 1])
            circuit.insert(X(target))
            circuit.insert(controlled_circuit(left_circuit, [target]))
            circuit.insert(X(target))

        if norm_right > 0:
            right_state = [a / norm_right for a in right]
            right_circuit = build_state_circuit(right_state, qs[:m - 1])
            circuit.insert(controlled_circuit(right_circuit, [target]))

        return circuit

    return build_state_circuit(amplitudes, qubits)
