# EVAL_META: task_id=78, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def qft_no_swaps(num_qubits):
    circuit = pq.QCircuit()
    if num_qubits <= 0:
        return circuit

    machine = pq.CPUQVM()
    for _name in ("init_qvm", "initQVM", "init"):
        _method = getattr(machine, _name, None)
        if callable(_method):
            try:
                _method()
                break
            except Exception:
                pass

    if hasattr(machine, "qAlloc_many"):
        qubits = list(machine.qAlloc_many(num_qubits))
    elif hasattr(machine, "qalloc_many"):
        qubits = list(machine.qalloc_many(num_qubits))
    elif hasattr(machine, "qAllocMany"):
        qubits = list(machine.qAllocMany(num_qubits))
    else:
        _alloc = getattr(machine, "qAlloc", None) or getattr(machine, "qalloc")
        qubits = [_alloc() for _ in range(num_qubits)]

    if not hasattr(qft_no_swaps, "_machines"):
        qft_no_swaps._machines = []
    qft_no_swaps._machines.append(machine)

    def _append(node):
        nonlocal circuit
        try:
            result = circuit.__lshift__(node)
            if result is not None:
                circuit = result
            return
        except Exception:
            pass
        result = circuit.insert(node)
        if result is not None:
            circuit = result

    def _cnot(control, target):
        gate = getattr(pq, "CNOT", None) or getattr(pq, "CX", None)
        if gate is not None:
            _append(gate(control, target))
        else:
            x_gate = pq.X(target)
            controlled = x_gate.control([control])
            _append(controlled)

    def _controlled_phase(control, target, angle):
        for gate_name in ("CP", "CR"):
            gate = getattr(pq, gate_name, None)
            if gate is not None:
                for args in ((control, target, angle), (angle, control, target)):
                    try:
                        _append(gate(*args))
                        return
                    except Exception:
                        pass

        phase = getattr(pq, "P", None) or getattr(pq, "U1", None)
        if phase is not None:
            _append(phase(control, angle / 2.0))
            _cnot(control, target)
            _append(phase(target, -angle / 2.0))
            _cnot(control, target)
            _append(phase(target, angle / 2.0))
        else:
            _append(pq.RZ(control, angle / 2.0))
            _append(pq.RZ(target, angle / 2.0))
            _cnot(control, target)
            _append(pq.RZ(target, -angle / 2.0))
            _cnot(control, target)

    for target in range(num_qubits):
        for control in range(target):
            _controlled_phase(
                qubits[control],
                qubits[target],
                -math.pi / (2 ** (target - control)),
            )
        _append(pq.H(qubits[target]))

    return circuit
