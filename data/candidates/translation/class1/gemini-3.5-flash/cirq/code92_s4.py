# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1)
    )
    sim = cirq.Simulator()
    result = sim.simulate(circuit, qubit_order=[q1, q0])
    state_vector = result.state_vector()
    probabilities = np.abs(state_vector) ** 2
    probabilities_dict = {}
    for i, prob in enumerate(probabilities):
        if prob > 1e-10:
            bitstring = format(i, '02b')
            probabilities_dict[bitstring] = float(prob)
    return probabilities_dict
