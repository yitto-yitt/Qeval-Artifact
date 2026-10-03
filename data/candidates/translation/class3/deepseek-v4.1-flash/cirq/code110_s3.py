# EVAL_META: task_id=110, framework=cirq, class=3
import cirq

def equivalent_clifford_circuit(circuit, n):
    original_qubits = sorted(circuit.all_qubits())
    num_qubits = len(original_qubits)
    op_or = cirq.unitary(circuit)
    qc_list = []
    counter = 0
    while counter < n:
        tableau = cirq.CliffordTableau.random(num_qubits)
        random_circuit = tableau.to_circuit()
        qubit_map = {cirq.LineQubit(i): original_qubits[i] for i in range(num_qubits)}
        qc = random_circuit.transform_qubits(qubit_map)
        op_qc = cirq.unitary(qc)
        if cirq.allclose_up_to_global_phase(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
