# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit, ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    for instruction in circuit.data:
        params = instruction.operation.params
        has_free = any(
            isinstance(p, ParameterExpression) and len(p.parameters) > 0
            for p in params
        )
        if not has_free:
            new_circuit.append(instruction.operation, instruction.qubits, instruction.clbits)
    return new_circuit
