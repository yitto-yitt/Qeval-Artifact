# EVAL_META: task_id=50, framework=qiskit, class=3
from qiskit import QuantumCircuit

def remove_gate_in_position(circuit, position):
    new_circuit = QuantumCircuit(circuit.num_qubits, circuit.num_clbits)
    for i, instr in enumerate(circuit.data):
        if i != position:
            new_circuit.append(instr.operation, instr.qubits, instr.clbits)
    return new_circuit
