# EVAL_META: task_id=99, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    new_circ = circuit.copy()
    new_circ.data.clear()
    
    for instruction in circuit.data:
        if isinstance(instruction, tuple):
            inst, qargs, cargs = instruction
        else:
            inst = instruction.operation
            
        has_unassigned = False
        for p in inst.params:
            if isinstance(p, ParameterExpression):
                if len(p.parameters) > 0:
                    has_unassigned = True
                    break
                    
        if not has_unassigned:
            if isinstance(instruction, tuple):
                new_circ.append(*instruction)
            else:
                new_circ.append(instruction)
                
    return new_circ
