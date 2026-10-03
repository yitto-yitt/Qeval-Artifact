# EVAL_META: task_id=77, framework=qpanda, class=1
import math

from pyqpanda3.core import *


def circuit_from_probability_dist(probability_dist):
    def _new_circuit():
        try:
            return QCircuit()
        except TypeError:
            return QCircuit(num_qubits)

    def _append(circuit, operation):
        try:
            result = circuit.insert(operation)
            return circuit if result is None else result
        except Exception:
            result = circuit << operation
            return circuit if result is None else result

    def _controlled_gate(gate, controls):
        if not controls:
            return gate
        try:
            result = gate.control(controls)
            return gate if result is None else result
        except Exception:
            ctrl_func = globals().get("control", None) or globals().get("Control", None)
            if ctrl_func is not None:
                return ctrl_func(gate, controls)
            raise

    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    probabilities = [probability_dist.get(basis_state, 0) for basis_state in range(2 ** num_qubits)]

    qubits = list(range(num_qubits))
    try:
        RY(qubits[0], 0.0)
    except Exception:
        machine = CPUQVM()
        for init_name in ("init_qvm", "initQVM", "init"):
            if hasattr(machine, init_name):
                getattr(machine, init_name)()
                break
        qubits = list(machine.qAlloc_many(num_qubits))
        if not hasattr(circuit_from_probability_dist, "_machines"):
            circuit_from_probability_dist._machines = []
        circuit_from_probability_dist._machines.append(machine)

    circuit = _new_circuit()

    for qubit in qubits:
        circuit = _append(circuit, RY(qubit, 0.0))

    for level in range(num_qubits):
        target_bit = num_qubits - 1 - level
        target_qubit = qubits[target_bit]
        control_bits = [num_qubits - 1 - i for i in range(level)]
        control_qubits = [qubits[bit] for bit in control_bits]

        for prefix in range(1 << level):
            total_zero = 0.0
            total_one = 0.0

            for lower in range(1 << target_bit):
                zero_index = (prefix << (target_bit + 1)) | lower
                one_index = zero_index | (1 << target_bit)
                total_zero += probabilities[zero_index]
                total_one += probabilities[one_index]

            if total_zero == 0 and total_one == 0:
                continue

            angle = 2.0 * math.atan2(math.sqrt(total_one), math.sqrt(total_zero))
            if angle == 0.0:
                continue

            zero_controls = []
            for idx, control_qubit in enumerate(control_qubits):
                desired_bit = (prefix >> (level - 1 - idx)) & 1
                if desired_bit == 0:
                    zero_controls.append(control_qubit)

            for control_qubit in zero_controls:
                circuit = _append(circuit, X(control_qubit))

            gate = _controlled_gate(RY(target_qubit, angle), control_qubits)
            circuit = _append(circuit, gate)

            for control_qubit in reversed(zero_controls):
                circuit = _append(circuit, X(control_qubit))

    return circuit
