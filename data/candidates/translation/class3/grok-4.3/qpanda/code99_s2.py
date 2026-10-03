# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import Parameter, QuantumCircuit

def remove_unassigned_parameterized_gates(circuit):
    circuit_data = circuit.data.copy()
    circuit_without_params = QuantumCircuit(circuit.num_qubits, circuit.num_clbits)
    
    for instruction in circuit_data:
        instr, qargs, cargs = instruction.operation, instruction.qubits, instruction.clbits
        if not (isinstance(instr.params, Parameter) or 
                isinstance(instr.params[0], Parameter) if len(instr.params) > 0 else False):
            circuit_without_params.append(instr, qargs, cargs)

    return circuit_without_params
