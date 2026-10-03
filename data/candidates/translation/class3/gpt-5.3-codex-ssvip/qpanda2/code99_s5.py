# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(16)

def remove_unassigned_parameterized_gates(circuit):
    prog = pq.QProg()
    for gate in circuit:
        params = []
        if isinstance(gate, dict):
            params = gate.get("params", [])
        else:
            params = getattr(gate, "params", [])
        has_unassigned = False
        if params is not None and len(params) > 0:
            for p in params:
                if p is None:
                    has_unassigned = True
                    break
                if isinstance(p, str):
                    has_unassigned = True
                    break
                if hasattr(p, "name") and not isinstance(p, (int, float, complex)):
                    has_unassigned = True
                    break
        if not has_unassigned:
            if isinstance(gate, pq.QGate):
                prog.insert(gate)
            elif isinstance(gate, dict) and "gate" in gate and isinstance(gate["gate"], pq.QGate):
                prog.insert(gate["gate"])
    machine.finalize()
    return prog
