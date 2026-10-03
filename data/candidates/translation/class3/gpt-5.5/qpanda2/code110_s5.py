# EVAL_META: task_id=110, framework=qpanda2, class=3
import random
import re
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(64)
atexit.register(lambda: machine.finalize())

def equivalent_clifford_circuit(circuit, n):
    def _qid(qubit):
        for name in ("get_phy_addr", "getPhysicalQubitPtr"):
            try:
                return getattr(qubit, name)()
            except Exception:
                pass
        return repr(qubit)

    def _unique_qubits(qubits):
        out = []
        seen = set()
        for qb in qubits:
            key = _qid(qb)
            if key not in seen:
                seen.add(key)
                out.append(qb)
        return out

    def _used_qubits(obj):
        for name in ("get_used_qubits", "get_all_used_qubits"):
            try:
                val = getattr(obj, name)()
                val = list(val)
                if val:
                    return _unique_qubits(val)
            except Exception:
                pass

        for func_name in ("get_all_used_qubits", "get_qprog_used_qubits"):
            try:
                val = getattr(pq, func_name)(obj)
                val = list(val)
                if val:
                    return _unique_qubits(val)
            except Exception:
                pass

        try:
            prog = pq.QProg()
            prog.insert(obj)
            ir = pq.convert_qprog_to_originir(prog, machine)
            inds = sorted({int(x) for x in re.findall(r"q\[(\d+)\]", ir)})
            if inds:
                need = max(inds) + 1
                if need > len(q):
                    return [q[i] for i in range(len(q))]
                return [q[i] for i in inds]
        except Exception:
            pass

        for attr in ("num_qubits", "qubit_num", "qubits_num"):
            try:
                cnt = getattr(obj, attr)
                if callable(cnt):
                    cnt = cnt()
                cnt = int(cnt)
                if cnt > 0:
                    return [q[i] for i in range(min(cnt, len(q)))]
            except Exception:
                pass

        for name in ("get_qubit_num", "get_qubits_num"):
            try:
                cnt = int(getattr(obj, name)())
                if cnt > 0:
                    return [q[i] for i in range(min(cnt, len(q)))]
            except Exception:
                pass

        return []

    def _insert_gate(circ, desc, qubits):
        name = desc[0]
        if name == "H":
            circ.insert(pq.H(qubits[desc[1]]))
        elif name == "S":
            circ.insert(pq.S(qubits[desc[1]]))
        elif name == "X":
            circ.insert(pq.X(qubits[desc[1]]))
        elif name == "Z":
            circ.insert(pq.Z(qubits[desc[1]]))
        elif name == "CNOT":
            circ.insert(pq.CNOT(qubits[desc[1]], qubits[desc[2]]))

    def _insert_inverse_gate(circ, desc, qubits):
        if desc[0] == "S":
            circ.insert(pq.S(qubits[desc[1]]))
            circ.insert(pq.S(qubits[desc[1]]))
            circ.insert(pq.S(qubits[desc[1]]))
        else:
            _insert_gate(circ, desc, qubits)

    def _new_container_like(obj):
        if "qprog" in obj.__class__.__name__.lower():
            return pq.QProg()
        return pq.QCircuit()

    qubits = _used_qubits(circuit)
    result = []
    counter = 0

    while counter < n:
        out = _new_container_like(circuit)
        try:
            out.insert(circuit)
        except Exception:
            try:
                tmp = pq.QProg()
                tmp.insert(circuit)
                out.insert(tmp)
            except Exception:
                pass

        if qubits:
            gate_seq = []
            depth = random.randint(max(1, len(qubits)), max(2, 4 * len(qubits) + 6))
            for _ in range(depth):
                if len(qubits) >= 2 and random.random() < 0.35:
                    a, b = random.sample(range(len(qubits)), 2)
                    gate_seq.append(("CNOT", a, b))
                else:
                    gate_seq.append((random.choice(("H", "S", "X", "Z")), random.randrange(len(qubits))))

            rand_circ = pq.QCircuit()
            inv_circ = pq.QCircuit()

            for desc in gate_seq:
                _insert_gate(rand_circ, desc, qubits)
            for desc in reversed(gate_seq):
                _insert_inverse_gate(inv_circ, desc, qubits)

            out.insert(rand_circ)
            out.insert(inv_circ)

        result.append(out)
        counter += 1

    return result
