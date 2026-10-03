# EVAL_META: task_id=11, framework=qpanda2, class=2
from pyqpanda import QCircuit, QProg, get_statevector as qpanda_get_statevector, get_used_qubits


def get_statevector(circuit):
    if isinstance(circuit, QCircuit):
        prog = QProg()
        prog << circuit
    else:
        prog = circuit

    qubits = get_used_qubits(prog)

    try:
        return qpanda_get_statevector(prog, qubits)
    except TypeError:
        return qpanda_get_statevector(prog)
