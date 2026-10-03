# EVAL_META: task_id=40, framework=cirq, class=1
import cirq
import numpy as np

def init_random_3qubit(desired_vector):
    qubits = cirq.LineQubit.range(3)
    prep = cirq.Circuit(cirq.StatePreparationChannel(desired_vector).on(*qubits))
    sim = cirq.Simulator()
    result = sim.simulate(prep)
    state = result.final_state_vector
    probs = np.abs(state) ** 2
    return {f'{i:03b}': float(p) for i, p in enumerate(probs)}
