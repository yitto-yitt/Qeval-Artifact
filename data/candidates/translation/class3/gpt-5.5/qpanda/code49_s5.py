# EVAL_META: task_id=49, framework=qpanda, class=3
import pyqpanda3.core as pq

def simple_elitzur_vaidman():
    def _append(circuit, gate):
        result = circuit << gate
        return circuit if result is None else result

    try:
        circuit = pq.QCircuit(2)

        h_method = getattr(circuit, "h", None)
        cnot_method = getattr(circuit, "cnot", None) or getattr(circuit, "cx", None)
        if callable(h_method) and callable(cnot_method):
            result = h_method(0)
            if result is not None:
                circuit = result
            cnot_method = getattr(circuit, "cnot", None) or getattr(circuit, "cx", None)
            result = cnot_method(0, 1)
            if result is not None:
                circuit = result
            h_method = getattr(circuit, "h", None)
            result = h_method(0)
            if result is not None:
                circuit = result
            return circuit

        h_gate = getattr(pq, "H")
        cnot_gate = getattr(pq, "CNOT", None) or getattr(pq, "CX")
        circuit = _append(circuit, h_gate(0))
        circuit = _append(circuit, cnot_gate(0, 1))
        circuit = _append(circuit, h_gate(0))
        return circuit
    except Exception:
        pass

    machine_cls = getattr(pq, "CPUQVM", None) or getattr(pq, "CPUSingleThreadQVM", None)
    machine = machine_cls()

    for init_name in ("init", "init_qvm"):
        init_method = getattr(machine, init_name, None)
        if callable(init_method):
            init_method()
            break

    alloc_method = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
        candidate = getattr(machine, alloc_name, None)
        if callable(candidate):
            alloc_method = candidate
            break

    qubits = alloc_method(2)
    circuit = pq.QCircuit()
    h_gate = getattr(pq, "H")
    cnot_gate = getattr(pq, "CNOT", None) or getattr(pq, "CX")

    circuit = _append(circuit, h_gate(qubits[0]))
    circuit = _append(circuit, cnot_gate(qubits[0], qubits[1]))
    circuit = _append(circuit, h_gate(qubits[0]))

    if not hasattr(simple_elitzur_vaidman, "_machines"):
        simple_elitzur_vaidman._machines = []
    simple_elitzur_vaidman._machines.append(machine)

    return circuit
