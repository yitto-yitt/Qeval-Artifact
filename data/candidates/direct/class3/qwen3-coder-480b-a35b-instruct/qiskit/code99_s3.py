# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.parameter import Parameter


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    
    for instruction in circuit.data:
        # Check if the instruction has any unassigned parameters
        has_unassigned_param = False
        for param in instruction.operation.params:
            if isinstance(param, Parameter):
                has_unassigned_param = True
                break
        
        # Only add the gate if it doesn't have unassigned parameters
        if not has_unassigned_param:
            new_circuit.append(instruction.operation, instruction.qubits, instruction.clbits)
    
    return new_circuit
