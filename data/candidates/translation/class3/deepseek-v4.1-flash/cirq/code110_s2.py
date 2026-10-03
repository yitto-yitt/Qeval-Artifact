# EVAL_META: task_id=110, framework=cirq, class=3
import cirq

def equivalent_clifford_circuit(circuit, n):
    target_unitary = cirq.unitary(circuit)
    num_qubits = circuit.num_qubits()
    result = []
    counter = 0
    while counter < n:
        random_circuit = cirq.CliffordTableau.random(num_qubits).to_circuit()
        try:
            random_unitary = cirq.unitary(random_circuit)
        except Exception:
            continue
        if cirq.allclose_up_to_global_phase(target_unitary, random_unitary, rtol=0.4, atol=0.4):
            result.append(random_circuit)
            counter += 1
    return result
