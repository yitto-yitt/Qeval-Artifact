# EVAL_META: task_id=77, framework=qpanda, class=1
import math
from pyqpanda3.core import *


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    dim = 2 ** num_qubits
    amplitudes = [math.sqrt(probability_dist.get(basis_state, 0)) for basis_state in range(dim)]
    weights = [amp * amp for amp in amplitudes]

    if not hasattr(circuit_from_probability_dist, "_qvm"):
        qvm = CPUQVM()
        try:
            qvm.init_qvm()
        except AttributeError:
            pass
        circuit_from_probability_dist._qvm = qvm

    qvm = circuit_from_probability_dist._qvm
    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(num_qubits)
    else:
        qubits = qvm.qalloc_many(num_qubits)

    circuit = QCircuit()

    def _append(cir, op):
        if hasattr(cir, "insert"):
            res = cir.insert(op)
            return cir if res is None else res
        res = cir << op
        return cir if res is None else res

    def _controlled(gate, controls):
        if controls:
            res = gate.control(controls)
            return gate if res is None else res
        return gate

    for q in qubits:
        circuit = _append(circuit, RY(q, 0.0))

    for level in range(num_qubits):
        target_bit = num_qubits - 1 - level

        for prefix in range(2 ** level):
            w0 = 0.0
            w1 = 0.0

            for basis_state in range(dim):
                if (basis_state >> (target_bit + 1)) == prefix:
                    if (basis_state >> target_bit) & 1:
                        w1 += weights[basis_state]
                    else:
                        w0 += weights[basis_state]

            if w0 + w1 == 0:
                continue

            theta = 2.0 * math.atan2(math.sqrt(w1), math.sqrt(w0))
            if theta == 0.0:
                continue

            controls = []
            zero_controls = []

            for bit_pos in range(num_qubits - 1, target_bit, -1):
                desired = (prefix >> (bit_pos - target_bit - 1)) & 1
                controls.append(qubits[bit_pos])
                if desired == 0:
                    zero_controls.append(qubits[bit_pos])

            for ctrl in zero_controls:
                circuit = _append(circuit, X(ctrl))

            circuit = _append(circuit, _controlled(RY(qubits[target_bit], theta), controls))

            for ctrl in zero_controls:
                circuit = _append(circuit, X(ctrl))

    return circuit
