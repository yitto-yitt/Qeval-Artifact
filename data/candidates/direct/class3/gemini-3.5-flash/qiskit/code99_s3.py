# EVAL_META: task_id=99, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit: QuantumCircuit) -> QuantumCircuit:
    new_circuit = circuit.copy()
    del new_circuit.data[:]
    
    for instruction in circuit.data:
        if isinstance(instruction, tuple):
            operation, qubits, clbits = instruction
        else:
            operation = instruction.operation
            qubits = instruction.qubits
            clbits = instruction.clbits
            
        has_unassigned = False
        if hasattr(operation, 'params'):
            for p in operation.params:
                if isinstance(p, ParameterExpression):
                    if len(p.parameters) > 0:
                        has_unassigned = True
                        break
        
        if not has_unassigned:
            new_circuit.append(operation, qubits, clbits)
            
    return new_circuit
