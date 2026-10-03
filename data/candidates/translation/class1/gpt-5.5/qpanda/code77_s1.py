# EVAL_META: task_id=77, framework=qpanda, class=1
import math

from pyqpanda3.core import *


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    probabilities = [probability_dist.get(i, 0) for i in range(2**num_qubits)]

    machine = CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(num_qubits)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(num_qubits)
    else:
        qubits = machine.qAllocMany(num_qubits)

    if not hasattr(circuit_from_probability_dist, "_machines"):
        circuit_from_probability_dist._machines = []
    circuit_from_probability_dist._machines.append(machine)

    circuit = QCircuit()

    def append(node):
        nonlocal circuit
        if hasattr(circuit, "insert"):
            circuit.insert(node)
        else:
            circuit = circuit << node

    def apply_controlled_ry(target, controls, pattern, angle):
        if abs(angle) < 1e-15:
            return

        zero_controls = []
        for j, control_qubit_index in enumerate(controls):
            if ((pattern >> j) & 1) == 0:
                zero_controls.append(control_qubit_index)
                append(X(qubits[control_qubit_index]))

        gate = RY(qubits[target], angle)
        if controls:
            controlled_gate = gate.control([qubits[i] for i in controls])
            if controlled_gate is not None:
                gate = controlled_gate
        append(gate)

        for control_qubit_index in reversed(zero_controls):
            append(X(qubits[control_qubit_index]))

    for target in range(num_qubits - 1, -1, -1):
        controls = list(range(target + 1, num_qubits))
        for pattern in range(2 ** len(controls)):
            p0 = 0.0
            p1 = 0.0
            for basis_state, probability in enumerate(probabilities):
                if (basis_state >> (target + 1)) == pattern:
                    if ((basis_state >> target) & 1) == 0:
                        p0 += probability
                    else:
                        p1 += probability

            if p0 + p1 > 0:
                angle = 2 * math.atan2(math.sqrt(p1), math.sqrt(p0))
                apply_controlled_ry(target, controls, pattern, angle)

    return circuit
