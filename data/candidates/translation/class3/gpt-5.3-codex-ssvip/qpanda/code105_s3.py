# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, QCircuit, CNOT, T, matrix_decompose


def initialize_cnot_dihedral():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)

    circuit = QCircuit()
    circuit.insert(CNOT(q[0], q[1]))
    circuit.insert(T(q[0]))

    prog = QProg()
    prog.insert(circuit)

    unitary = qvm.get_unitary(prog, q)
    result = {"circuit": circuit, "unitary": unitary}

    qvm.finalize()
    return result
