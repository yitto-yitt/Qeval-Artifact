# EVAL_META: task_id=119, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import CDKMRippleCarryAdder
def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    adder = CDKMRippleCarryAdder(num_state_qubits, kind=kind)
    qc = QuantumCircuit(adder.num_qubits)
    qc.append(adder.to_gate(), list(range(adder.num_qubits)))
    return qc
