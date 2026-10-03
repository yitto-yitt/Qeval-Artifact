# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np


def bell_dag():
    dev = qml.device('default.qubit', wires=3)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1, 2])
    
    tape = circuit.qtape
    
    # Create a DAG representation manually since PennyLane doesn't have direct DAG conversion
    ops = []
    for op in tape.operations:
        ops.append({
            'name': op.name,
            'wires': op.wires.tolist(),
            'params': op.parameters
        })
    
    measurements = []
    for m in tape.measurements:
        measurements.append({
            'name': m.return_type.name if hasattr(m.return_type, 'name') else str(m.return_type),
            'wires': m.wires.tolist() if m.wires else None
        })
    
    dag = {
        'operations': ops,
        'measurements': measurements,
        'wires': list(range(3))
    }
    
    return dag
