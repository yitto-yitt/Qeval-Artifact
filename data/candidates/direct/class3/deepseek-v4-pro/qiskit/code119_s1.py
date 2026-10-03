# EVAL_META: task_id=119, framework=qiskit, class=3

from qiskit.circuit.library import CDKMRippleCarryAdder


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    return CDKMRippleCarryAdder(num_state_qubits, kind=kind)
