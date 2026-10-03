# EVAL_META: task_id=99, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit: QuantumCircuit) -> QuantumCircuit:
    new_circuit = circuit.copy()
    new_circuit.clear()
    
    for inst in circuit.data:
        if isinstance(inst, tuple):
            operation, qargs, cargs = inst
        else:
            operation = inst.operation
            qargs = inst.qubits
            cargs = inst.clbits
            
        has_unassigned = False
        if hasattr(operation, 'params'):
            for param in operation.params:
                if isinstance(param, ParameterExpression):
                    if len(param.parameters) > 0:
                        has_unassigned = True
                        break
        if not has_unassigned:
            new_circuit.append(operation, qargs, cargs)
            
    return new_circuit
