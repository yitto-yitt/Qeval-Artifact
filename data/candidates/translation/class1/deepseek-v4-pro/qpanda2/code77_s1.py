# EVAL_META: task_id=77, framework=qpanda2, class=1
import builtins
import math

from pyqpanda import *


def circuit_from_probability_dist(probability_dist):
    init(QMachineType.CPU)
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1

    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    def norm(lst):
        return math.sqrt(builtins.sum(a * a for a in lst))

    total_norm = norm(amplitudes)
    if total_norm > 0:
        amplitudes = [a / total_norm for a in amplitudes]

    qubits = qAlloc_many(num_qubits)
    circuit = QCircuit()

    def add_ctrl_ry(circ, target, controls, control_states, theta):
        for q, state in zip(controls, control_states):
            if state == 0:
                circ << X(q)

        if not controls:
            circ << RY(target, theta)
        else:
            gate = RY(target, theta)
            gate = gate.control(controls)
            circ << gate

        for q, state in zip(controls, control_states):
            if state == 0:
                circ << X(q)

    def build_recursive(qubits, amps, controls, control_states, circ):
        if len(amps) <= 1:
            return

        half = len(amps) // 2
        first = amps[:half]
        second = amps[half:]

        p = norm(first)
        q = norm(second)
        theta = 2 * math.atan2(q, p)

        target = qubits[len(controls)]
        add_ctrl_ry(circ, target, controls, control_states, theta)

        build_recursive(qubits, first, controls + [target], control_states + [0], circ)
        build_recursive(qubits, second, controls + [target], control_states + [1], circ)

    build_recursive(qubits, amplitudes, [], [], circuit)
    return circuit
