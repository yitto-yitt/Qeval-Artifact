# EVAL_META: task_id=110, framework=cirq, class=3
import cirq

def equivalent_clifford_circuit(circuit, n):
    op_or = cirq.unitary(circuit)
    num_qubits = len(circuit.all_qubits())
    qc_list = []
    counter = 0
    while counter < n:
        cliff = cirq.random_clifford(num_qubits)
        qc = cliff.to_circuit()
        op_qc = cirq.unitary(qc)
        if cirq.allclose_up_to_global_phase(op_or, op_qc, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
