# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = circuit.copy_empty_like()
    for instr in circuit.data:
        if not any(isinstance(p, ParameterExpression) for p in instr.operation.params):
            new_circuit.append(instr.operation, instr.qubits, instr.clbits)
    return new_circuit
