# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    for gate in circuit.get_instructions():
        if hasattr(gate, 'get_params'):
            params = gate.get_params()
            has_unassigned = any(
                hasattr(p, 'is_parameter') and p.is_parameter()
                for p in params
            )
            if has_unassigned:
                continue
        new_circuit << gate
    return new_circuit
