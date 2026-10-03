# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QProg

_machine = CPUQVM()
_machine.init_qvm()
_q = _machine.qAlloc_many(1)

def remove_gate_in_position(circuit, position):
    node_iter = circuit.getFirstNodeIter()
    end_iter = circuit.getEndNodeIter()
    nodes = []
    while node_iter != end_iter:
        nodes.append(node_iter.getCurNode())
        node_iter.getNext()

    pos = position
    if pos < 0:
        pos += len(nodes)
    if pos < 0 or pos >= len(nodes):
        raise IndexError("list index out of range")

    if hasattr(circuit, "deleteNode"):
        node_iter = circuit.getFirstNodeIter()
        for _ in range(pos):
            node_iter.getNext()
        circuit.deleteNode(node_iter.getCurNode())
        return circuit

    new_circuit = QProg()
    for i, node in enumerate(nodes):
        if i != pos:
            new_circuit << node
    return new_circuit

_machine.finalize()
