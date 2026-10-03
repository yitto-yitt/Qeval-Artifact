# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def remove_unassigned_parameterized_gates(circuit):
    prog = pq.QProg()
    if circuit is None:
        machine.finalize()
        return prog

    for gate in circuit:
        params = []
        if hasattr(gate, "get_parameter"):
            try:
                params = gate.get_parameter()
            except Exception:
                params = []
        has_unassigned = False
        for p in params:
            if not isinstance(p, (int, float)):
                has_unassigned = True
                break
        if not has_unassigned:
            prog << gate

    machine.finalize()
    return prog
