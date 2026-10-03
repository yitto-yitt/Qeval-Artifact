# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
from cirq.testing import random_clifford_circuit

def equivalent_clifford_circuit(circuit: cirq.Circuit, n: int):
    qubits = sorted(list(circuit.all_qubits()))
    op_or = cirq.unitary(circuit)
    qc_list = []
    counter = 0
    while counter < n:
        qc = random_clifford_circuit(qubits, gate_count=10 * len(qubits))
        op_qc = cirq.unitary(qc)
        if cirq.equal_up_to_global_phase(op_qc, op_or, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
