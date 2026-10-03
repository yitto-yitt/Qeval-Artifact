# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1))
    state = cirq.final_state_vector(circuit)
    probs = np.abs(state) ** 2
    n = len(circuit.all_qubits())
    return {
        format(i, f'0{n}b'): round(float(probs[i]), 15)
        for i in range(2 ** n)
        if probs[i] > 1e-12
    }
