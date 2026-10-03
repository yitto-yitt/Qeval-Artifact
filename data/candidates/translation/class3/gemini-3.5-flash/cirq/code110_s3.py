# EVAL_META: task_id=110, framework=cirq, class=3
import cirq
import numpy as np
from cirq.testing import random_clifford_circuit

def equivalent_clifford_circuit(circuit: cirq.Circuit, n: int):
    qubits = sorted(list(circuit.all_qubits()))
    op_or = cirq.unitary(circuit, qubit_order=qubits)
    qc_list = []
    counter = 0
    while counter < n:
        gate_count = np.random.randint(5, 20)
        qc = random_clifford_circuit(qubits, gate_count=gate_count)
        op_qc = cirq.unitary(qc, qubit_order=qubits)
        if cirq.allclose_up_to_global_phase(op_or, op_qc, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
