# EVAL_META: task_id=110, framework=cirq, class=3
import cirq

def equivalent_clifford_circuit(circuit, n):
    op_or = cirq.unitary(circuit)
    num_qubits = circuit.num_qubits
    qc_list = []
    counter = 0
    while counter < n:
        rand_cliff = cirq.random_clifford(num_qubits)
        qubits = cirq.LineQubit.range(num_qubits)
        op = rand_cliff.on(*qubits)
        qc = cirq.Circuit(cirq.decompose(op))
        op_qc = cirq.unitary(qc)
        if cirq.allclose_up_to_global_phase(op_or, op_qc, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
