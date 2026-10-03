# EVAL_META: task_id=7, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_parametrized_gate():
    qvm = pq.CPUQVM()
    for init_name in ("init_qvm", "init"):
        if hasattr(qvm, init_name):
            try:
                getattr(qvm, init_name)()
                break
            except Exception:
                pass

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(1)
    elif hasattr(qvm, "qalloc_many"):
        qubits = qvm.qalloc_many(1)
    elif hasattr(qvm, "qAlloc"):
        qubits = [qvm.qAlloc()]
    else:
        qubits = [0]

    if not hasattr(create_parametrized_gate, "_machines"):
        create_parametrized_gate._machines = []
    create_parametrized_gate._machines.append(qvm)

    param_candidates = []
    for name in ("Parameter", "QParameter", "Variable", "Var"):
        if hasattr(pq, name):
            try:
                param_candidates.append(getattr(pq, name)("theta"))
            except Exception:
                pass
    if hasattr(pq, "var"):
        try:
            param_candidates.append(pq.var("theta"))
        except Exception:
            try:
                param_candidates.append(pq.var(0.0))
            except Exception:
                pass
    param_candidates.extend(["theta", 0.0])

    circuit = None
    for cls_name in ("QCircuit", "QProg"):
        if hasattr(pq, cls_name):
            try:
                circuit = getattr(pq, cls_name)()
                break
            except Exception:
                pass
    if circuit is None:
        circuit = pq.QProg()

    last_error = None
    for theta in param_candidates:
        gate_candidates = []
        try:
            gate_candidates.append(pq.RX(qubits[0], theta))
        except Exception as exc:
            last_error = exc
        try:
            gate_candidates.append(pq.RX(theta, qubits[0]))
        except Exception as exc:
            last_error = exc

        for gate in gate_candidates:
            try:
                updated = circuit << gate
                if updated is not None:
                    circuit = updated
                return circuit
            except Exception as exc:
                last_error = exc
                try:
                    updated = circuit.insert(gate)
                    if updated is not None:
                        circuit = updated
                    return circuit
                except Exception as exc2:
                    last_error = exc2

    raise last_error if last_error is not None else RuntimeError("Unable to create parameterized RX circuit")
