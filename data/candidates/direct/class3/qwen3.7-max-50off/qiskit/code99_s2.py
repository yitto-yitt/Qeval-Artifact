# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit, ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs, name=circuit.name)
    for inst in circuit.data:
        if not any(isinstance(p, ParameterExpression) for p in inst.operation.params):
            new_circuit.append(inst.operation, inst.qubits, inst.clbits)
    return new_circuit
