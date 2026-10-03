# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml
from pennylane import numpy as np

def get_statevector(circuit):
    # Convert the input circuit to a PennyLane tape
    if isinstance(circuit, qml.tape.QuantumTape):
        tape = circuit
    else:
        # Assume circuit is a function that creates operations
        with qml.tape.QuantumTape() as tape:
            circuit()
    
    # Create a device with enough wires
    num_wires = max([op.wires[0] for op in tape.operations]) + 1 if tape.operations else 1
    dev = qml.device('default.qubit', wires=num_wires)
    
    # Execute the tape on the device to get the state vector
    state = dev.execute(tape)
    return state
