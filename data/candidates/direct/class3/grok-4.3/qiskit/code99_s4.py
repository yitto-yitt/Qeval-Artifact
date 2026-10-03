# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QuantumCircuit(circuit.num_qubits, circuit.num_clbits)
    for instruction in circuit.data:
        op = instruction.operation
        has_unassigned = False
        for param in op.params:
            if isinstance(param, ParameterExpression) and len(param.parameters) > 0:
                has_unassigned = True
                break
        if not has_unassigned:
            new_circuit.append(op, instruction.qubits, instruction.clbits)
    return new_circuit
