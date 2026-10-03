# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import *

def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.get_qubit_num()
    target_mat = circuit.get_matrix()
    result = []
    while len(result) < n:
        qvm = CPUQVM()
        qvm.init_qvm()
        q = qvm.qAlloc_many(num_qubits)
        prog = QProg()
        for i in range(num_qubits):
            prog << H(q[i])
            prog << S(q[i])
            prog << X(q[i])
            prog << Z(q[i])
        if num_qubits >= 2:
            for i in range(num_qubits - 1):
                prog << CNOT(q[i], q[i + 1])
        cand_mat = get_matrix(prog)
        if matrix_compare(cand_mat, target_mat, 0.4, 0.4):
            result.append(prog)
        qvm.finalize()
    return result
