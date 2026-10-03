# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    for pauli_str, t in zip(pauli_strings, times):
        time_per_step = t / reps
        # phase exponent for e^{-i*t/reps * P}
        # e^{-i * time_per_step * P} = e^{i * pi * (-time_per_step/pi) * P}
        phase_exponent = -time_per_step / np.pi
        pauli_string = cirq.DensePauliString(pauli_str).on(*qubits)
        op = pauli_string.exponential(phase_exponent=phase_exponent)
        for _ in range(reps):
            circuit.append(op)
    return circuit
