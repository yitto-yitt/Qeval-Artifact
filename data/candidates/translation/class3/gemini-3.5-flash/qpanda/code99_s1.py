# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import *

def remove_unassigned_parameterized_gates(circuit):
    def is_unassigned_parameterized(gate):
        try:
            params = gate.get_gate_parameter()
            if isinstance(params, list):
                p_list = params
            elif hasattr(params, 'getParameter'):
                p_list = params.getParameter()
            elif hasattr(params, 'get_parameter'):
                p_list = params.get_parameter()
            else:
                p_list = []
                
            for p in p_list:
                p_type_name = type(p).__name__
                if p_type_name in ['Parameter', 'Expression', 'var']:
                    return True
        except Exception:
            pass
        return False

    if isinstance(circuit, QCircuit):
        new_circuit = QCircuit()
    else:
        new_circuit = QProg()

    def traverse(node):
        node_type = node.get_node_type()
        if node_type == NodeType.GATE_NODE:
            gate = cast_node_to_gate(node)
            if not is_unassigned_parameterized(gate):
                new_circuit.insert(gate)
        elif node_type == NodeType.CIRCUIT_NODE:
            cir = cast_node_to_circuit(node)
            for sub_node in cir:
                traverse(sub_node)
        elif node_type == NodeType.PROG_NODE:
            prog = cast_node_to_prog(node)
            for sub_node in prog:
                traverse(sub_node)

    for node in circuit:
        traverse(node)

    return new_circuit
