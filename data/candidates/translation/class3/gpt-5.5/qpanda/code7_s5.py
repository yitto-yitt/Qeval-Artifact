# EVAL_META: task_id=7, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq

def create_parametrized_gate():
    machine = pq.CPUQVM() if hasattr(pq, "CPUQVM") else pq.init_quantum_machine(pq.QMachineType.CPU)
    for init_name in ("init_qvm", "initQVM", "init"):
        if hasattr(machine, init_name):
            try:
                getattr(machine, init_name)()
                break
            except TypeError:
                pass

    qubits = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "alloc_many_qubit", "qAllocMany"):
        if hasattr(machine, alloc_name):
            try:
                qubits = getattr(machine, alloc_name)(1)
                break
            except TypeError:
                pass
    if qubits is None:
        for alloc_name in ("qAlloc", "qalloc", "allocate_qubit", "alloc_qubit"):
            if hasattr(machine, alloc_name):
                qubits = [getattr(machine, alloc_name)()]
                break
    if qubits is None:
        raise RuntimeError("Unable to allocate qubit in pyqpanda3.")

    parameter_candidates = []
    for cls_name in ("Parameter", "QParameter", "ParameterExpression", "Var", "Variable"):
        if hasattr(pq, cls_name):
            cls = getattr(pq, cls_name)
            for args, kwargs in (
                (("theta",), {}),
                ((), {"name": "theta"}),
                ((0.0,), {}),
                ((), {}),
            ):
                try:
                    parameter_candidates.append(cls(*args, **kwargs))
                    break
                except Exception:
                    continue

    if hasattr(pq, "var"):
        for args in (
            ("theta",),
            (0.0, True),
            (np.array([0.0]), True),
            (np.array([[0.0]]), True),
        ):
            try:
                parameter_candidates.append(pq.var(*args))
            except Exception:
                pass

    last_error = None
    for theta in parameter_candidates:
        try:
            quantum_circuit = pq.QCircuit()
            gate = pq.RX(qubits[0], theta)
            try:
                inserted = quantum_circuit << gate
                if inserted is not None:
                    quantum_circuit = inserted
            except Exception:
                inserted = quantum_circuit.insert(gate)
                if inserted is not None:
                    quantum_circuit = inserted
            return quantum_circuit
        except Exception as exc:
            last_error = exc

    for theta in parameter_candidates:
        for circuit_cls_name in ("VariationalQuantumCircuit", "VQC"):
            for gate_cls_name in ("VariationalQuantumGate_RX", "VQG_RX"):
                if hasattr(pq, circuit_cls_name) and hasattr(pq, gate_cls_name):
                    try:
                        quantum_circuit = getattr(pq, circuit_cls_name)()
                        gate = getattr(pq, gate_cls_name)(qubits[0], theta)
                        inserted = quantum_circuit.insert(gate)
                        if inserted is not None:
                            quantum_circuit = inserted
                        return quantum_circuit
                    except Exception as exc:
                        last_error = exc

    if last_error is not None:
        raise last_error
    raise RuntimeError("Unable to create parametrized RX gate in pyqpanda3.")
