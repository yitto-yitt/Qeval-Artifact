# EVAL_META: task_id=117, framework=cirq, class=3
import numpy as np
import cirq

def decompose_unitary(unitary):
    q = cirq.LineQubit.range(2)
    mat = np.asarray(unitary, dtype=complex)
    ops = cirq.two_qubit_matrix_to_cz_operations(
        q[0], q[1], mat,
        allow_partial_czs=False,
        clean_single_qubit_operations=True,
    )
    converted = []
    for op in ops:
        if op.gate == cirq.CZ:
            a, b = op.qubits
            converted.append(cirq.H.on(b))
            converted.append(cirq.CNOT.on(a, b))
            converted.append(cirq.H.on(b))
        else:
            converted.append(op)
    circuit = cirq.Circuit(converted)
    if len(circuit.all_qubits()) < 2:
        for qubit in q:
            if qubit not in circuit.all_qubits():
                circuit.append(cirq.I.on(qubit))
    return circuit
