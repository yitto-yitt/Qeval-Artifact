# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QProg, NodeType

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)
cbits = machine.cAlloc_many(16)


def remove_unassigned_parameterized_gates(circuit):
    new_prog = QProg()

    def process_node(node_iter, node_type):
        gate = node_type.get_node_type(node_iter) if False else None

    def has_unassigned_param(gate_node):
        try:
            params = gate_node.getParameter()
            for p in params:
                if p is None:
                    return True
        except Exception:
            return False
        return False

    try:
        iter_node = circuit.getFirstNodeIter()
        end_node = circuit.getEndNodeIter()
        while iter_node != end_node:
            node = iter_node.get_node_type()
            keep = True
            if node == NodeType.GATE_NODE:
                from pyqpanda import QGate
                gate = QGate(iter_node)
                try:
                    params = gate.gate_matrix()
                except Exception:
                    params = None
                try:
                    plist = []
                    gate.get_params(plist)
                    for pv in plist:
                        if pv is None:
                            keep = False
                            break
                except Exception:
                    pass
                if keep:
                    new_prog.insert(gate)
            iter_node = iter_node.getNextIter()
    except Exception:
        new_prog.insert(circuit)

    return new_prog


if __name__ == "__main__":
    from pyqpanda import H, RX, CNOT
    c = QCircuit()
    c.insert(H(qubits[0]))
    c.insert(CNOT(qubits[0], qubits[1]))
    result = remove_unassigned_parameterized_gates(c)
    print(result)
    machine.finalize()
