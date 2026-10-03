# EVAL_META: task_id=77, framework=qpanda, class=1
import math

from pyqpanda3.core import CPUQVM, QCircuit, RY, X

_QPANDA_MACHINES = []


def _init_machine():
    machine = CPUQVM()
    for name in ("init_qvm", "initQVM", "init"):
        method = getattr(machine, name, None)
        if method is not None:
            try:
                method()
            except Exception:
                pass
            break
    _QPANDA_MACHINES.append(machine)
    return machine


def _alloc_qubits(machine, num_qubits):
    for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qalloc_many"):
        method = getattr(machine, name, None)
        if method is not None:
            qvec = method(num_qubits)
            return [qvec[i] for i in range(num_qubits)]

    for name in ("qAlloc", "qalloc"):
        method = getattr(machine, name, None)
        if method is not None:
            return [method() for _ in range(num_qubits)]

    raise RuntimeError("Unable to allocate qubits in pyqpanda3 CPUQVM")


def _append(circuit, node):
    try:
        circuit << node
    except Exception:
        circuit.insert(node)


def _controlled_ry(circuit, qubits, target_index, theta, controls):
    zero_controls = [idx for idx, value in controls if value == 0]

    for idx in zero_controls:
        _append(circuit, X(qubits[idx]))

    gate = RY(qubits[target_index], float(theta))
    if controls:
        control_qubits = [qubits[idx] for idx, _ in controls]
        controlled_gate = gate.control(control_qubits)
        if controlled_gate is not None:
            gate = controlled_gate

    _append(circuit, gate)

    for idx in reversed(zero_controls):
        _append(circuit, X(qubits[idx]))


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    machine = _init_machine()
    qubits = _alloc_qubits(machine, num_qubits)
    circuit = QCircuit()

    def prepare(vector, bit_positions, controls):
        if not bit_positions:
            return

        target_index = bit_positions[0]
        half = len(vector) // 2

        left = vector[:half]
        right = vector[half:]

        norm_left = math.sqrt(sum(x * x for x in left))
        norm_right = math.sqrt(sum(x * x for x in right))

        theta = 2.0 * math.atan2(norm_right, norm_left)
        if abs(theta) > 1e-15:
            _controlled_ry(circuit, qubits, target_index, theta, controls)

        remaining = bit_positions[1:]

        if norm_left > 1e-15:
            prepare([x / norm_left for x in left], remaining, controls + [(target_index, 0)])

        if norm_right > 1e-15:
            prepare([x / norm_right for x in right], remaining, controls + [(target_index, 1)])

    prepare(amplitudes, list(range(num_qubits - 1, -1, -1)), [])
    return circuit
