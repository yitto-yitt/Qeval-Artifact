# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))

    result = cirq.Simulator().simulate(circuit)
    state = result.final_state_vector
    probs = np.abs(state) ** 2

    qubits = sorted(circuit.all_qubits())
    n = len(qubits)
    probabilities_dict = {}
    for i, p in enumerate(probs):
        if p > 1e-10:
            bitstring = format(i, f'0{n}b')
            probabilities_dict[bitstring] = float(p)
    return probabilities_dict
