# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X, H

def create_custom_controlled():
    # Create the 2-qubit gate: X on qubit 0, H on qubit 1
    sub_circ = QCircuit()
    sub_circ << X(0) << H(1)
    # Add 2 control qubits to the gate
    controlled_gate = sub_circ.control(2)
    # Create the 4-qubit circuit and apply the gate with mapping [control0, control1, target0, target1] = [0,3,1,2]
    circuit = QCircuit()
    circuit << controlled_gate([0, 3, 1, 2])
    return circuit
