# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1])
    )
    
    simulator = cirq.Simulator()
    result = simulator.simulate(circuit)
    state_vector = result.final_state_vector
    probabilities = np.abs(state_vector)**2
    
    prob_dict = {}
    for i, p in enumerate(probabilities):
        if p > 1e-9:
            bitstring = format(i, '02b')
            prob_dict[bitstring] = float(np.round(p, 5))
            
    return prob_dict
