# EVAL_META: task_id=119, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import CDKMRippleCarryAdder

def create_ripple_carry_adder_circuit(num_state_qubits: int, kind: str) -> QuantumCircuit:
    adder = CDKMRippleCarryAdder(num_state_qubits, kind=kind)
    qc = QuantumCircuit(adder.num_qubits)
    qc.append(adder, range(adder.num_qubits))
    return qc
