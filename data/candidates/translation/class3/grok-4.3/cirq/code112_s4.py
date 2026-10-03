# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    if not pauli_strings:
        return cirq.Circuit()
    n_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    symbol_map = {'I': cirq.I, 'X': cirq.X, 'Y': cirq.Y, 'Z': cirq.Z}
    for pauli_string, time in zip(pauli_strings, times):
        pauli_dict = {qubits[i]: symbol_map[p] for i, p in enumerate(pauli_string) if p != 'I'}
        if not pauli_dict:
            continue
        ps = cirq.PauliString(pauli_dict)
        delta_time = time / reps if reps > 0 else time
        exponent = 2 * delta_time / np.pi
        for _ in range(reps):
            circuit.append(cirq.PauliStringPhasor(ps, exponent=exponent))
    return circuit
