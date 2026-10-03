# EVAL_META: task_id=112, framework=qpanda2, class=3
import math
from pyqpanda import *

MAX_QUBITS = 64
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(MAX_QUBITS)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    if not pauli_strings:
        return QCircuit()
    num_qubits = len(pauli_strings[0])
    if num_qubits > MAX_QUBITS:
        raise ValueError("Number of qubits exceeds MAX_QUBITS")
    q_local = [q[i] for i in range(num_qubits)]
    circuit = QCircuit()

    for pauli_string, time in zip(pauli_strings, times):
        step_time = time / reps
        for _ in range(reps):
            non_i_positions = []
            for idx, ch in enumerate(pauli_string):
                if ch == 'I':
                    continue
                non_i_positions.append(idx)
                if ch == 'X':
                    circuit << H(q_local[idx])
                elif ch == 'Y':
                    circuit << RX(q_local[idx], math.pi / 2.0)
                elif ch == 'Z':
                    pass
                else:
                    raise ValueError(f"Invalid Pauli character: {ch}")

            if len(non_i_positions) > 1:
                for i in range(len(non_i_positions) - 1):
                    circuit << CNOT(q_local[non_i_positions[i]], q_local[non_i_positions[i + 1]])

            if len(non_i_positions) >= 1:
                circuit << RZ(q_local[non_i_positions[-1]], 2.0 * step_time)

            if len(non_i_positions) > 1:
                for i in reversed(range(len(non_i_positions) - 1)):
                    circuit << CNOT(q_local[non_i_positions[i]], q_local[non_i_positions[i + 1]])

            for idx in reversed(range(len(pauli_string))):
                ch = pauli_string[idx]
                if ch == 'X':
                    circuit << H(q_local[idx])
                elif ch == 'Y':
                    circuit << RX(q_local[idx], -math.pi / 2.0)

    return circuit

machine.finalize()
