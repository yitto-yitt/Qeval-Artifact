# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import Parameter, QCircuit

def remove_unassigned_parameterized_gates(circuit):
    circuit_data = circuit.data.copy()
    circuit_without_params = QCircuit(circuit.num_qubits, circuit.num_clbits)
    
    for instruction in circuit_data:
        instr, qargs, cargs = instruction.operation, instruction.qubits, instruction.clbits
        if not (isinstance(instr.params, Parameter) or 
                isinstance(instr.params[0], Parameter)):
            circuit_without_params.append(instr, qargs, cargs)

    return circuit_without_params
