# EVAL_META: task_id=92, framework=cirq, class=1
import cirq

def calculate_stabilizer_state_info():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
    )
    sim = cirq.Simulator()
    result = sim.simulate(circuit)
    probs = result.state_vector()
    return {
        "00": float(abs(probs[0]) ** 2),
        "01": float(abs(probs[1]) ** 2),
        "10": float(abs(probs[2]) ** 2),
        "11": float(abs(probs[3]) ** 2),
    }
