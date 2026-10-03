# EVAL_META: task_id=92, framework=cirq, class=1
import cirq


def calculate_stabilizer_state_info():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
    )
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit)
    probs = result.state_vector().reshape(2, 2)
    probabilities_dict = {}
    for i in range(2):
        for j in range(2):
            p = abs(probs[i, j]) ** 2
            if p > 0:
                probabilities_dict[f"{i}{j}"] = float(p)
    return probabilities_dict
