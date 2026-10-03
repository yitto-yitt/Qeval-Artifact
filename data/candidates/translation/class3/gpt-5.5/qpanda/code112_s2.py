# EVAL_META: task_id=112, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    machine = None

    for cls_name in ("CPUQVM", "CPUSingleThreadQVM"):
        cls = getattr(pq, cls_name, None)
        if cls is not None:
            try:
                machine = cls()
                break
            except Exception:
                machine = None

    if machine is not None:
        for init_name in ("init_qvm", "initQVM", "init"):
            init_fn = getattr(machine, init_name, None)
            if init_fn is not None:
                try:
                    init_fn()
                    break
                except Exception:
                    pass

    qubits = None
    if machine is not None:
        for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits", "allocateQubits"):
            alloc_fn = getattr(machine, alloc_name, None)
            if alloc_fn is not None:
                try:
                    qubits = alloc_fn(n)
                    break
                except Exception:
                    qubits = None
        if qubits is None:
            alloc_one = getattr(machine, "qAlloc", None)
            if alloc_one is not None:
                qubits = [alloc_one() for _ in range(n)]

    if qubits is None:
        alloc_many = getattr(pq, "qAlloc_many", None)
        if alloc_many is not None:
            qubits = alloc_many(n)
        else:
            qubits = list(range(n))

    try:
        if not hasattr(create_product_formula_circuit, "_qpanda_context"):
            create_product_formula_circuit._qpanda_context = []
        create_product_formula_circuit._qpanda_context.append((machine, qubits))
    except Exception:
        pass

    circuit = pq.QCircuit()

    def append_gate(gate):
        nonlocal circuit
        try:
            result = circuit.__lshift__(gate)
            if result is not None:
                circuit = result
            return
        except Exception:
            pass
        try:
            result = circuit.insert(gate)
            if result is not None:
                circuit = result
            return
        except Exception:
            pass
        result = circuit.append(gate)
        if result is not None:
            circuit = result

    def cnot_gate(control, target):
        if hasattr(pq, "CNOT"):
            return pq.CNOT(control, target)
        return pq.CX(control, target)

    reps_int = int(reps)

    for pauli_string, time in zip(pauli_strings, times):
        label = str(pauli_string).upper()
        active = []
        pauli_by_qubit = {}
        for pos, char in enumerate(label):
            q_index = n - 1 - pos
            if char not in ("I", "X", "Y", "Z"):
                raise ValueError("Invalid Pauli string")
            pauli_by_qubit[q_index] = char
            if char != "I":
                active.append(q_index)

        active.sort()

        for _ in range(reps_int):
            angle = 2.0 * float(time) / reps_int

            for q_index in active:
                char = pauli_by_qubit[q_index]
                if char == "X":
                    append_gate(pq.H(qubits[q_index]))
                elif char == "Y":
                    append_gate(pq.RX(qubits[q_index], -math.pi / 2.0))

            for i in range(len(active) - 1):
                append_gate(cnot_gate(qubits[active[i]], qubits[active[i + 1]]))

            if active:
                append_gate(pq.RZ(qubits[active[-1]], angle))
            else:
                if n > 0 and hasattr(pq, "I"):
                    append_gate(pq.I(qubits[0]))

            for i in range(len(active) - 2, -1, -1):
                append_gate(cnot_gate(qubits[active[i]], qubits[active[i + 1]]))

            for q_index in reversed(active):
                char = pauli_by_qubit[q_index]
                if char == "X":
                    append_gate(pq.H(qubits[q_index]))
                elif char == "Y":
                    append_gate(pq.RX(qubits[q_index], math.pi / 2.0))

    return circuit
