# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1))
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit)
    probs = np.abs(result.final_state_vector)**2
    return {
        '00': float(probs[0]),
        '01': float(probs[1]),
        '10': float(probs[2]),
        '11': float(probs[3])
    }
