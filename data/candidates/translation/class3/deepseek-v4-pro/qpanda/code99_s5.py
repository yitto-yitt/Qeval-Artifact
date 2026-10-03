# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QProg, QCircuit

def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, QCircuit):
        new_circuit = QCircuit()
    else:
        new_circuit = QProg()

    gates = circuit.getQGateList()
    for gate in gates:
        params = gate.getParameter()
        if not isinstance(params, (list, tuple)):
            params = [params]
        has_unassigned = False
        for p in params:
            if not isinstance(p, (int, float, complex)):
                has_unassigned = True
                break
        if not has_unassigned:
            new_circuit << gate

    return new_circuit
