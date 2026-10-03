# EVAL_META: task_id=99, framework=qpanda, class=3
import pyqpanda3.core as pq

def remove_unassigned_parameterized_gates(circuit):
    def is_unassigned(gate):
        def is_param_obj(x):
            name = type(x).__name__
            return name in ('Parameter', 'var', 'Var', 'Expression')

        for attr in dir(gate):
            if attr.startswith('__'):
                continue
            try:
                val = getattr(gate, attr)
                if is_param_obj(val):
                    return True
                if hasattr(val, '__iter__') and not isinstance(val, (str, bytes)):
                    try:
                        for item in val:
                            if is_param_obj(item):
                                return True
                    except Exception:
                        pass
                if callable(val):
                    try:
                        res = val()
                        if is_param_obj(res):
                            return True
                    except Exception:
                        pass
            except Exception:
                pass
        return False

    try:
        def filter_prog(prog):
            new_prog = pq.QProg()
            it = prog.begin()
            while it != prog.end():
                node = it.get_current_node()
                node_type = node.get_node_type()
                if node_type == pq.NodeType.GATE_NODE:
                    gate = pq.CastToQGate(node)
                    if not is_unassigned(gate):
                        new_prog.insert(gate)
                elif node_type == pq.NodeType.CIRCUIT_NODE:
                    cir = pq.CastToQCircuit(node)
                    new_prog.insert(filter_circuit(cir))
                elif node_type == pq.NodeType.PROG_NODE:
                    p = pq.CastToQProg(node)
                    new_prog.insert(filter_prog(p))
                elif node_type == pq.NodeType.MEASURE_GATE:
                    measure = pq.CastToQMeasure(node)
                    new_prog.insert(measure)
                else:
                    new_prog.insert(node)
                it.next()
            return new_prog

        def filter_circuit(cir):
            new_cir = pq.QCircuit()
            it = cir.begin()
            while it != cir.end():
                node = it.get_current_node()
                node_type = node.get_node_type()
                if node_type == pq.NodeType.GATE_NODE:
                    gate = pq.CastToQGate(node)
                    if not is_unassigned(gate):
                        new_cir.insert(gate)
                elif node_type == pq.NodeType.CIRCUIT_NODE:
                    sub_cir = pq.CastToQCircuit(node)
                    new_cir.insert(filter_circuit(sub_cir))
                else:
                    new_cir.insert(node)
                it.next()
            return new_cir

        if isinstance(circuit, pq.QCircuit):
            return filter_circuit(circuit)
        elif isinstance(circuit, pq.QProg):
            return filter_prog(circuit)
    except Exception:
        pass

    try:
        new_circuit = type(circuit)()
        insert_func = getattr(new_circuit, 'insert', getattr(new_circuit, 'append', None))
        
        items = []
        if hasattr(circuit, '_nodes'):
            items = circuit._nodes
        elif hasattr(circuit, '_gates'):
            items = circuit._gates
        else:
            try:
                items = list(circuit)
            except Exception:
                pass
                
        for item in items:
            if not is_unassigned(item):
                if insert_func:
                    insert_func(item)
        return new_circuit
    except Exception:
        pass

    return circuit
