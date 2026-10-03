# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)
cbits = machine.cAlloc_many(16)


def remove_unassigned_parameterized_gates(circuit):
    new_prog = QProg()
    for node_iter in circuit:
        node_type = node_iter.get_node_type()
        if node_type == NodeType.GATE_NODE:
            gate = QGate(node_iter)
            keep = True
            try:
                params = gate.gate_matrix()
                if hasattr(gate, 'get_parameter'):
                    p = gate.get_parameter()
                    if p is None:
                        keep = False
            except Exception:
                keep = True
            if keep:
                new_prog.insert(gate)
        else:
            new_prog.insert(node_iter)
    return new_prog


machine.finalize()
