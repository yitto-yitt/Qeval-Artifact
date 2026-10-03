# EVAL_META: task_id=110, framework=cirq, class=3
import cirq

def equivalent_clifford_circuit(circuit, n):
    num_qubits = len(circuit.all_qubits())
    target_unitary = cirq.unitary(circuit)
    result = []
    while len(result) < n:
        tableau = cirq.CliffordTableau.random(num_qubits)
        rand_circuit = tableau.to_circuit()
        rand_unitary = cirq.unitary(rand_circuit)
        if cirq.allclose_up_to_global_phase(target_unitary, rand_unitary, atol=0.4, rtol=0.4):
            result.append(rand_circuit)
    return result
