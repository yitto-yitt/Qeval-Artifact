# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = circuit.copy_empty_like()
    for instruction in circuit.data:
        op = instruction.operation
        has_unassigned = any(
            isinstance(p, ParameterExpression) and len(p.parameters) > 0
            for p in op.params
        )
        if not has_unassigned:
            new_circuit.append(op, instruction.qubits, instruction.clbits)
    return new_circuit
