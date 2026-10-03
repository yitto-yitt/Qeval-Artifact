# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit, ParameterExpression

def _has_unassigned_parameters(instruction):
    for param in instruction.operation.params:
        if isinstance(param, ParameterExpression) and param.parameters:
            return True
    return False

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = circuit.copy_empty_like()
    for instruction in circuit.data:
        if not _has_unassigned_parameters(instruction):
            new_circuit.append(instruction.operation, instruction.qubits, instruction.clbits)
    return new_circuit
