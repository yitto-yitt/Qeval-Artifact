# EVAL_META: task_id=110, framework=cirq, class=3
import cirq

def equivalent_clifford_circuit(circuit, n):
    op_or = cirq.unitary(circuit)
    num_qubits = circuit.num_qubits()
    qc_list = []
    counter = 0
    while counter < n:
        qc = cirq.CliffordTableau.random(num_qubits).to_circuit()
        op_qc = cirq.unitary(qc)
        if cirq.allclose_up_to_global_phase(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
