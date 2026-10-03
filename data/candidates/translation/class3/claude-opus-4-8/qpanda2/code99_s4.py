# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QProg

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)


def remove_unassigned_parameterized_gates(circuit):
    result = QCircuit()
    if hasattr(circuit, "__iter__"):
        for node in circuit:
            params = None
            if hasattr(node, "gate_matrix"):
                try:
                    params = node.get_params()
                except Exception:
                    params = None
            has_unassigned = False
            if isinstance(node, dict):
                params = node.get("params")
                if params is not None:
                    for p in params:
                        if p is None or isinstance(p, str):
                            has_unassigned = True
                            break
                if not has_unassigned:
                    result.insert(node.get("gate"))
            else:
                result.insert(node)
    else:
        result = circuit
    return result


machine.finalize()
