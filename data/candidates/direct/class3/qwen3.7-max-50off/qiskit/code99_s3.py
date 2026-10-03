# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = circuit.copy_empty_like()
    for inst in circuit.data:
        if isinstance(inst, tuple):
            op, qargs, cargs = inst
        else:
            op = inst.operation
            qargs = inst.qubits
            cargs = inst.clbits
        
        has_unassigned = False
        for p in op.params:
            if isinstance(p, ParameterExpression) and p.parameters:
                has_unassigned = True
                break
                
        if not has_unassigned:
            new_circuit.append(op, qargs, cargs)
            
    return new_circuit
