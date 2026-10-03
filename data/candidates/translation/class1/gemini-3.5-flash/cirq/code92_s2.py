# EVAL_META: task_id=92, framework=cirq, class=1
import cirq
import numpy as np

def calculate_stabilizer_state_info():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1)
    )
    
    # Qiskit uses LSB-first ordering (qubit 0 is the rightmost bit).
    # In Cirq, we achieve this by ordering the qubits in reverse: [q1, q0].
    state_vector = cirq.final_state_vector(circuit, qubit_order=[q1, q0])
    
    probabilities_dict = {}
    n_qubits = 2
    for i, amp in enumerate(state_vector):
        prob = float(np.abs(amp)**2)
        if prob > 1e-10:
            bitstring = bin(i)[2:].zfill(n_qubits)
            probabilities_dict[bitstring] = prob
            
    return probabilities_dict
