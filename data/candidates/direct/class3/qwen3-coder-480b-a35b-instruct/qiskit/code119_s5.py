# EVAL_META: task_id=119, framework=qiskit, class=3
from qiskit.circuit.library import CDKMRippleCarryAdder
from qiskit import QuantumCircuit


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    adder = CDKMRippleCarryAdder(num_state_qubits, kind=kind)
    circuit = QuantumCircuit(adder.num_qubits)
    circuit.compose(adder, inplace=True)
    return circuit
