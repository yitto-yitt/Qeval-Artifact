# EVAL_META: task_id=125, framework=qiskit, class=3

from qiskit.converters import circuit_to_gate


def circ_to_gate(circ):
    circ_gate = circuit_to_gate(circ)
    return circ_gate


# ==================================================
