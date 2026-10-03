# EVAL_META: task_id=109, framework=qpanda, class=3
import pyqpanda3.core as pq

def circuit():
    global _task109_machine, _task109_qubits
    machine = pq.CPUQVM()
    for init_name in ("init_qvm", "initQVM", "init"):
        if hasattr(machine, init_name):
            try:
                getattr(machine, init_name)()
            except TypeError:
                pass
            break

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(1)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(1)
    elif hasattr(machine, "qAllocMany"):
        qubits = machine.qAllocMany(1)
    else:
        qubits = [machine.qAlloc()]

    theta_candidates = []
    for name in ("Parameter", "ParameterExpression", "Var"):
        if hasattr(pq, name):
            try:
                theta_candidates.append(getattr(pq, name)("th"))
            except Exception:
                pass
    if hasattr(pq, "var"):
        try:
            theta_candidates.append(pq.var(0.0, True))
        except Exception:
            pass
    theta_candidates.append(0.0)

    last_error = None
    for theta in theta_candidates:
        try:
            qc = pq.QCircuit()
            qc << pq.H(qubits[0])
            qc << pq.RZ(qubits[0], theta)
            _task109_machine = machine
            _task109_qubits = qubits
            return qc
        except Exception as exc:
            last_error = exc

    if hasattr(pq, "VariationalQuantumCircuit") and hasattr(pq, "VQG_H") and hasattr(pq, "VQG_RZ"):
        for theta in theta_candidates:
            try:
                qc = pq.VariationalQuantumCircuit()
                qc << pq.VQG_H(qubits[0])
                qc << pq.VQG_RZ(qubits[0], theta)
                _task109_machine = machine
                _task109_qubits = qubits
                return qc
            except Exception as exc:
                last_error = exc

    raise last_error
