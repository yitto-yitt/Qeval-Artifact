# EVAL_META: task_id=119, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import CDKMRippleCarryAdder


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    adder = CDKMRippleCarryAdder(num_state_qubits=num_state_qubits, kind=kind)
    circuit = QuantumCircuit(*adder.qregs)
    circuit.append(adder.to_gate(), circuit.qubits)
    return circuit
