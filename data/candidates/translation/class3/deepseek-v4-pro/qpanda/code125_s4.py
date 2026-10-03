# EVAL_META: task_id=125, framework=qpanda, class=3
from pyqpanda3.core import QProg, prog_to_qgate


def circ_to_gate(circ):
    if isinstance(circ, QProg):
        prog = circ
    else:
        prog = QProg()
        prog << circ

    qubits = list(circ.get_used_qubits())
    return prog_to_qgate(prog, qubits)
