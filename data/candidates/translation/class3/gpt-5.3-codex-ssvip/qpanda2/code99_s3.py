# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(32)

def remove_unassigned_parameterized_gates(circuit):
    prog = pq.QProg()
    if circuit is None:
        return prog
    for gate in circuit:
        keep_gate = True
        try:
            params = gate.getParameter()
            if params is not None and len(params) > 0:
                for p in params:
                    if isinstance(p, str):
                        keep_gate = False
                        break
                    if hasattr(p, "isVariable") and p.isVariable():
                        keep_gate = False
                        break
                    if hasattr(p, "expr") and p.expr is not None:
                        keep_gate = False
                        break
        except Exception:
            keep_gate = True
        if keep_gate:
            prog.insert(gate)
    machine.finalize()
    return prog
