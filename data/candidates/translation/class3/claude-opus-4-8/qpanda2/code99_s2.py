# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)
cbits = machine.cAlloc_many(16)


def remove_unassigned_parameterized_gates(circuit):
    new_prog = pq.QProg()
    for node_iter in circuit:
        gate = pq.QGate(node_iter)
        has_unassigned = False
        try:
            params = gate.gate_matrix()
        except Exception:
            params = None
        node_type = node_iter.get_node_type()
        if node_type == pq.NodeType.GATE_NODE:
            g = pq.QGate(node_iter)
            gate_type = g.gate_type()
            try:
                angle_params = []
                if hasattr(g, "get_parameter"):
                    angle_params = g.get_parameter()
                is_parametric = gate_type in (
                    pq.GateType.RX_GATE,
                    pq.GateType.RY_GATE,
                    pq.GateType.RZ_GATE,
                    pq.GateType.U1_GATE,
                    pq.GateType.U2_GATE,
                    pq.GateType.U3_GATE,
                    pq.GateType.U4_GATE,
                    pq.GateType.CPHASE_GATE,
                    pq.GateType.ISWAP_THETA_GATE,
                )
                unassigned = False
                if is_parametric:
                    vals = g.get_parameter() if hasattr(g, "get_parameter") else []
                    if isinstance(vals, (list, tuple)):
                        for v in vals:
                            if v is None:
                                unassigned = True
                    elif vals is None:
                        unassigned = True
                has_unassigned = unassigned
            except Exception:
                has_unassigned = False
            if not has_unassigned:
                new_prog << g
        else:
            new_prog << node_iter
    return new_prog


machine.finalize()
