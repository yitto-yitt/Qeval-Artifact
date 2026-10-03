# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QProg, QCircuit

def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, QCircuit):
        new_circuit = QCircuit()
        new_circuit.insert(circuit)
        return new_circuit
    elif isinstance(circuit, QProg):
        new_circuit = QProg()
        new_circuit.insert(circuit)
        return new_circuit
    return circuit
