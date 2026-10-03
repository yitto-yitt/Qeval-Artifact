# EVAL_META: task_id=99, framework=pennylane, class=3
import pennylane as qml

def remove_unassigned_parameterized_gates(circuit):
    circuit_data = circuit.operations.copy()
    new_ops = []
    for instruction in circuit_data:
        params = instruction.parameters
        if len(params) == 0 or isinstance(params[0], (int, float)):
            new_ops.append(instruction)
    new_circuit = qml.tape.QuantumTape(ops=new_ops, measurements=circuit.measurements)
    return new_circuit
