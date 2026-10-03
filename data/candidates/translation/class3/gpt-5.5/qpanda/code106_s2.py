# EVAL_META: task_id=106, framework=qpanda, class=3
import pyqpanda3.core as pq


def compose_cnot_dihedral():
    def new_circuit():
        circuit_cls = getattr(pq, "QCircuit")
        try:
            return circuit_cls(2)
        except Exception:
            return circuit_cls()

    def append(obj, item):
        try:
            result = obj.__lshift__(item)
            return obj if result is None else result
        except Exception:
            if hasattr(obj, "insert"):
                result = obj.insert(item)
                return obj if result is None else result
            raise

    def build(qubits):
        circ1 = new_circuit()
        circ1 = append(circ1, pq.CNOT(qubits[0], qubits[1]))
        circ1 = append(circ1, pq.T(qubits[0]))

        circ2 = new_circuit()
        circ2 = append(circ2, pq.CNOT(qubits[0], qubits[1]))
        circ2 = append(circ2, pq.T(qubits[0]))
        circ2 = append(circ2, pq.X(qubits[1]))

        composed = new_circuit()
        composed = append(composed, circ1)
        composed = append(composed, circ2)
        return composed

    try:
        return build([0, 1])
    except Exception:
        machine = None
        for name in ("CPUQVM", "CPUSingleThreadQVM", "QVM"):
            if hasattr(pq, name):
                try:
                    machine = getattr(pq, name)()
                    break
                except Exception:
                    machine = None
        if machine is not None:
            for init_name in ("init_qvm", "init", "initQVM"):
                if hasattr(machine, init_name):
                    try:
                        getattr(machine, init_name)()
                    except Exception:
                        pass
                    break
            for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
                if hasattr(machine, alloc_name):
                    qubits = getattr(machine, alloc_name)(2)
                    compose_cnot_dihedral._machine = machine
                    return build(qubits)

        if hasattr(pq, "init"):
            try:
                pq.init()
            except Exception:
                pass
        qubits = pq.qAlloc_many(2)
        return build(qubits)
