# EVAL_META: task_id=110, framework=cirq, class=3
import cirq

def equivalent_clifford_circuit(circuit, n):
    qubits = sorted(circuit.all_qubits())
    num_qubits = len(qubits)
    op_or = cirq.unitary(circuit)
    qc_list = []
    counter = 0
    while counter < n:
        tableau = cirq.CliffordTableau.random(num_qubits)
        qc = tableau.to_circuit()
        qc_mapped = qc.transform_qubits(lambda q: qubits[q.x])
        op_qc = cirq.unitary(qc_mapped)
        if cirq.allclose_up_to_global_phase(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc_mapped)
    return qc_list
