# EVAL_META: task_id=119, framework=qpanda, class=3

from qiskit.circuit.library import CDKMRippleCarryAdder
from qiskit import QuantumCircuit
from qbraid import transpile

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    adder = CDKMRippleCarryAdder(num_state_qubits, kind)
    qc = QuantumCircuit(adder.num_qubits)
    qc.append(adder.to_instruction(), range(adder.num_qubits))
    return transpile(qc, "pyqpanda3")
