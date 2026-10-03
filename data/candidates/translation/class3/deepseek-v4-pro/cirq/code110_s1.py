# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
from cirq.testing import random_clifford

def equivalent_clifford_circuit(circuit, n):
    u_or = cirq.unitary(circuit)
    num_qubits = len(circuit.all_qubits())
    qc_list = []
    counter = 0
    while counter < n:
        cliff_gate = random_clifford(num_qubits)
        qc = cirq.Circuit(cliff_gate.on(*cirq.LineQubit.range(num_qubits)))
        u_qc = cirq.unitary(qc)
        if cirq.linalg.allclose_up_to_global_phase(u_or, u_qc, rtol=0.4, atol=0.4):
            qc_list.append(qc)
            counter += 1
    return qc_list
