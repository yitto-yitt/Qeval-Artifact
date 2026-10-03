# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def remove_unassigned_parameterized_gates(circuit):
    if circuit is None:
        return None

    if not hasattr(circuit, "get_ops"):
        return circuit

    new_prog = pq.QProg()
    for op in circuit.get_ops():
        params = []
        if hasattr(op, "get_parameters"):
            try:
                params = op.get_parameters()
            except Exception:
                params = []

        has_unassigned = False
        for p in params:
            if p is None:
                has_unassigned = True
                break
            if isinstance(p, str):
                has_unassigned = True
                break
            if hasattr(p, "is_variable") and callable(getattr(p, "is_variable")):
                try:
                    if p.is_variable():
                        has_unassigned = True
                        break
                except Exception:
                    pass

        if not has_unassigned:
            new_prog << op

    machine.finalize()
    return new_prog
