# EVAL_META: task_id=112, framework=qpanda, class=3
import math
from pyqpanda3.core import *

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    repetitions = int(reps)
    if repetitions < 1:
        raise ValueError("reps must be a positive integer")

    def _init_machine_and_qubits(num_qubits):
        qvm = None
        try:
            qvm = CPUQVM()
            initialized = False
            for init_name in ("init_qvm", "init", "initQVM"):
                if hasattr(qvm, init_name):
                    getattr(qvm, init_name)()
                    initialized = True
                    break

            for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
                if hasattr(qvm, alloc_name):
                    return qvm, list(getattr(qvm, alloc_name)(num_qubits))

            for alloc_name in ("qAlloc", "qalloc"):
                if hasattr(qvm, alloc_name):
                    alloc = getattr(qvm, alloc_name)
                    return qvm, [alloc() for _ in range(num_qubits)]
        except Exception:
            pass

        return None, list(range(num_qubits))

    def _new_circuit():
        try:
            return QCircuit()
        except TypeError:
            return QCircuit(n)

    def _append(circuit_obj, gate_obj):
        result = circuit_obj << gate_obj
        return circuit_obj if result is None else result

    def _rz_gate(qubit, angle):
        last_error = None
        for name in ("RZ", "RZGate"):
            if name in globals():
                try:
                    return globals()[name](qubit, angle)
                except Exception as exc:
                    last_error = exc
        if last_error is not None:
            raise last_error
        raise NameError("RZ gate is not available")

    def _h_gate(qubit):
        return H(qubit)

    def _cnot_gate(control, target):
        last_error = None
        for name in ("CNOT", "CX"):
            if name in globals():
                try:
                    return globals()[name](control, target)
                except Exception as exc:
                    last_error = exc
        try:
            gate = X(target)
            if hasattr(gate, "control"):
                return gate.control([control])
            if hasattr(gate, "set_control"):
                gate.set_control([control])
                return gate
        except Exception as exc:
            last_error = exc
        if last_error is not None:
            raise last_error
        raise NameError("CNOT/CX gate is not available")

    qvm, qubits = _init_machine_and_qubits(n)
    if qvm is not None:
        if not hasattr(create_product_formula_circuit, "_qpanda_machines"):
            create_product_formula_circuit._qpanda_machines = []
        create_product_formula_circuit._qpanda_machines.append(qvm)

    qc = _new_circuit()

    for i in range(n):
        qc = _append(qc, _rz_gate(qubits[i], 0.0))

    for pauli_string, time in zip(pauli_strings, times):
        label = str(pauli_string).upper()
        m = len(label)
        theta = time / repetitions

        active = []
        for pos, char in enumerate(label):
            if char != "I":
                active.append((m - 1 - pos, char))

        for _ in range(repetitions):
            for logical_index, char in active:
                qb = qubits[logical_index]
                if char == "X":
                    qc = _append(qc, _h_gate(qb))
                elif char == "Y":
                    qc = _append(qc, _rz_gate(qb, -math.pi / 2))
                    qc = _append(qc, _h_gate(qb))
                elif char == "Z":
                    pass
                else:
                    raise ValueError("Invalid Pauli character: " + char)

            if active:
                target_index = active[-1][0]
                target = qubits[target_index]

                for logical_index, _ in active[:-1]:
                    qc = _append(qc, _cnot_gate(qubits[logical_index], target))

                qc = _append(qc, _rz_gate(target, 2 * theta))

                for logical_index, _ in reversed(active[:-1]):
                    qc = _append(qc, _cnot_gate(qubits[logical_index], target))

            for logical_index, char in reversed(active):
                qb = qubits[logical_index]
                if char == "X":
                    qc = _append(qc, _h_gate(qb))
                elif char == "Y":
                    qc = _append(qc, _h_gate(qb))
                    qc = _append(qc, _rz_gate(qb, math.pi / 2))

    return qc
