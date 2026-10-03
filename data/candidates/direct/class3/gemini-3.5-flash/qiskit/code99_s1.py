# EVAL_META: task_id=99, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit: QuantumCircuit) -> QuantumCircuit:
    new_qc = circuit.copy()
    new_qc.data = []
    
    for instruction in circuit.data:
        if hasattr(instruction, 'operation'):
            operation = instruction.operation
            qargs = instruction.qubits
            cargs = instruction.clbits
        else:
            operation, qargs, cargs = instruction
        
        has_unassigned = False
        if hasattr(operation, 'params'):
            for p in operation.params:
                if isinstance(p, ParameterExpression):
                    if len(p.parameters) > 0:
                        has_unassigned = True
                        break
        
        if not has_unassigned:
            new_qc.append(operation, qargs, cargs)
            
    return new_qc
