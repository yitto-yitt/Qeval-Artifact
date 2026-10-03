# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1])
    )
    simulator = cirq.CliffordSimulator()
    result = simulator.simulate(circuit)
    state_vector = result.state.state_vector()
    prob_dict = {}
    for i, amp in enumerate(state_vector):
        p = float(np.abs(amp)**2)
        if p > 1e-10:
            bitstring = format(i, '02b')
            prob_dict[bitstring] = p
    return prob_dict
