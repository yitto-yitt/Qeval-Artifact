# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import CPUQVM

_qvm = CPUQVM()
_qvm.init_qvm()
_qubits = _qvm.qAlloc_many(1)

def remove_gate_in_position(circuit, position):
    nodes = list(circuit)
    if position < 0:
        position += len(nodes)
    if position < 0 or position >= len(nodes):
        raise IndexError("position out of range")

    new_circuit = type(circuit)()
    for i, node in enumerate(nodes):
        if i != position:
            new_circuit << node
    return new_circuit

_qvm.finalize()
