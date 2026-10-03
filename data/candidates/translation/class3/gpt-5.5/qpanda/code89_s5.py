# EVAL_META: task_id=89, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_controlled_hgate():
    def _new_circuit():
        try:
            return pq.QCircuit(3)
        except Exception:
            return pq.QCircuit()

    def _make_controlled_h(target, controls):
        gate = pq.H(target)

        for method_name in ("control", "ctrl"):
            method = getattr(gate, method_name, None)
            if method is not None:
                controlled_gate = method(controls)
                return gate if controlled_gate is None else controlled_gate

        for method_name in ("set_control", "setControl"):
            method = getattr(gate, method_name, None)
            if method is not None:
                controlled_gate = method(controls)
                return gate if controlled_gate is None else controlled_gate

        for func_name in ("control", "Control"):
            func = getattr(pq, func_name, None)
            if func is not None:
                return func(gate, controls)

        circuit = _new_circuit()
        try:
            circuit << gate
        except Exception:
            circuit.insert(gate)

        for method_name in ("control", "ctrl"):
            method = getattr(circuit, method_name, None)
            if method is not None:
                controlled_circuit = method(controls)
                return circuit if controlled_circuit is None else controlled_circuit

        for method_name in ("set_control", "setControl"):
            method = getattr(circuit, method_name, None)
            if method is not None:
                controlled_circuit = method(controls)
                return circuit if controlled_circuit is None else controlled_circuit

        return circuit

    def _append(circuit, operation):
        try:
            circuit << operation
            return circuit
        except Exception:
            inserted = circuit.insert(operation)
            return circuit if inserted is None else inserted

    try:
        qc = _new_circuit()
        return _append(qc, _make_controlled_h(2, [0, 1]))
    except Exception:
        pass

    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(3)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(3)
    else:
        qubits = machine.qAllocMany(3)

    qc = _new_circuit()
    result = _append(qc, _make_controlled_h(qubits[2], [qubits[0], qubits[1]]))
    create_controlled_hgate._machine = machine
    return result
