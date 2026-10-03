# EVAL_META: task_id=71, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def create_quantum_circuit_based_h0_csx01_h1():
    machine = None
    qubits = None

    if hasattr(pq, "CPUQVM"):
        machine = pq.CPUQVM()
        for init_name in ("init_qvm", "initQVM", "init"):
            if hasattr(machine, init_name):
                try:
                    getattr(machine, init_name)()
                    break
                except TypeError:
                    continue

        for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany"):
            if hasattr(machine, alloc_name):
                qubits = getattr(machine, alloc_name)(3)
                break
        if qubits is None:
            for alloc_name in ("qAlloc", "qalloc"):
                if hasattr(machine, alloc_name):
                    qubits = [getattr(machine, alloc_name)() for _ in range(3)]
                    break

    if qubits is None:
        if hasattr(pq, "init") and hasattr(pq, "QMachineType"):
            try:
                pq.init(pq.QMachineType.CPU)
            except Exception:
                pass
        if hasattr(pq, "qAlloc_many"):
            qubits = pq.qAlloc_many(3)
        else:
            qubits = [pq.qAlloc() for _ in range(3)]

    try:
        circuit = pq.QCircuit()
    except Exception:
        circuit = pq.QProg()

    def add(container, op):
        if hasattr(container, "insert"):
            try:
                res = container.insert(op)
                return container if res is None or res is True else res
            except Exception:
                pass
        res = container << op
        return container if res is None or res is True else res

    def phase_gate(q, theta):
        for name in ("P", "Phase", "U1"):
            if hasattr(pq, name):
                try:
                    return getattr(pq, name)(q, theta)
                except Exception:
                    pass
        return pq.RZ(q, theta)

    def cnot_gate(c, t):
        for name in ("CNOT", "CX"):
            if hasattr(pq, name):
                try:
                    return getattr(pq, name)(c, t)
                except Exception:
                    pass
        return pq.CNOT(c, t)

    circuit = add(circuit, pq.H(qubits[0]))

    used_direct_csx = False
    for name in ("CSX", "CSXGate"):
        if hasattr(pq, name):
            try:
                circuit = add(circuit, getattr(pq, name)(qubits[0], qubits[1]))
                used_direct_csx = True
                break
            except Exception:
                pass

    if not used_direct_csx:
        theta = math.pi / 2.0
        circuit = add(circuit, pq.H(qubits[1]))
        circuit = add(circuit, phase_gate(qubits[0], theta / 2.0))
        circuit = add(circuit, phase_gate(qubits[1], theta / 2.0))
        circuit = add(circuit, cnot_gate(qubits[0], qubits[1]))
        circuit = add(circuit, phase_gate(qubits[1], -theta / 2.0))
        circuit = add(circuit, cnot_gate(qubits[0], qubits[1]))
        circuit = add(circuit, pq.H(qubits[1]))

    circuit = add(circuit, pq.H(qubits[1]))

    refs = getattr(create_quantum_circuit_based_h0_csx01_h1, "_qpanda_refs", [])
    refs.append((machine, qubits))
    setattr(create_quantum_circuit_based_h0_csx01_h1, "_qpanda_refs", refs)

    return circuit
