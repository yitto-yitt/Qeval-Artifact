# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(1)

def remove_gate_in_position(circuit, position):
    gates = [circuit.getNodeByPosition(i) for i in range(circuit.getNodeCount())]
    new_circuit = QCircuit()
    for i, gate in enumerate(gates):
        if i != position:
            new_circuit.pushBackNode(gate)
    return new_circuit

machine.finalize()
