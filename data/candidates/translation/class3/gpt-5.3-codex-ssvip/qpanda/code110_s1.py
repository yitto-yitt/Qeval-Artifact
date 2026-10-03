# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import Clifford, matrix_decompose_qr


def equivalent_clifford_circuit(circuit, n):
    op_or = Clifford(circuit).get_matrix()
    num_qubits = circuit.get_qgate_num() if hasattr(circuit, "get_qgate_num") else circuit.get_qubit_num()
    qc_list = []
    counter = 0
    while counter < n:
        qc = Clifford.random(num_qubits).to_qprog()
        op_qc = Clifford(qc).get_matrix()
        if Clifford.matrix_equiv(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
