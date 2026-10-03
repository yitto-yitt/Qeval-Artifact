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
    probabilities_dict = {}
    for i, amp in enumerate(probs):
        p = float(abs(amp) ** 2)
        if p > 0:
            bitstring = format(i, "02b")
            probabilities_dict[bitstring] = p
    return probabilities_dict
