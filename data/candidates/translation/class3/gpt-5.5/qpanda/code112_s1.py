# EVAL_META: task_id=112, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])

    if not hasattr(create_product_formula_circuit, "_machine"):
        machine = pq.CPUQVM()
        if hasattr(machine, "init_qvm"):
            machine.init_qvm()
        create_product_formula_circuit._machine = machine

    machine = create_product_formula_circuit._machine

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(n_qubits)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(n_qubits)
    elif hasattr(machine, "qAllocMany"):
        qubits = machine.qAllocMany(n_qubits)
    else:
        qubits = [machine.qAlloc() for _ in range(n_qubits)]

    circuit = pq.QCircuit()

    for pauli_string, time in zip(pauli_strings, times):
        dt = float(time) / reps

        for _ in range(reps):
            active = []

            for i, pauli_char in enumerate(pauli_string):
                qidx = n_qubits - 1 - i
                p = pauli_char.upper()

                if p == "X":
                    circuit << pq.H(qubits[qidx])
                    active.append(qidx)
                elif p == "Y":
                    circuit << pq.RZ(qubits[qidx], -math.pi / 2)
                    circuit << pq.H(qubits[qidx])
                    active.append(qidx)
                elif p == "Z":
                    active.append(qidx)

            if len(active) == 1:
                circuit << pq.RZ(qubits[active[0]], 2.0 * dt)
            elif len(active) > 1:
                for j in range(len(active) - 1):
                    circuit << pq.CNOT(qubits[active[j]], qubits[active[j + 1]])

                circuit << pq.RZ(qubits[active[-1]], 2.0 * dt)

                for j in range(len(active) - 2, -1, -1):
                    circuit << pq.CNOT(qubits[active[j]], qubits[active[j + 1]])

            for i in range(len(pauli_string) - 1, -1, -1):
                qidx = n_qubits - 1 - i
                p = pauli_string[i].upper()

                if p == "X":
                    circuit << pq.H(qubits[qidx])
                elif p == "Y":
                    circuit << pq.H(qubits[qidx])
                    circuit << pq.RZ(qubits[qidx], math.pi / 2)

    return circuit
