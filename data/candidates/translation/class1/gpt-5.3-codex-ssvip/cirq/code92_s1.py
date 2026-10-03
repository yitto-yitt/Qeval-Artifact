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
    state = result.final_state_vector
    probs = {}
    for i, amp in enumerate(state):
        p = abs(amp) ** 2
        if p > 0:
            probs[format(i, "02b")] = float(p)
    return probs
