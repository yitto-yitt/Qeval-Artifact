# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(16)

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "data"):
        del circuit.data[position]
        return circuit

    try:
        del circuit[position]
        return circuit
    except Exception:
        pass

    method_names = ("erase", "delete_node", "deleteQNode", "delete_qnode", "remove")

    for name in method_names:
        if hasattr(circuit, name):
            try:
                getattr(circuit, name)(position)
                return circuit
            except Exception:
                pass

    pos = position
    if pos < 0:
        try:
            pos = len(circuit) + pos
        except Exception:
            count = 0
            try:
                it = circuit.begin()
                end = circuit.end()
                while it != end:
                    count += 1
                    if hasattr(it, "get_next"):
                        it = it.get_next()
                    elif hasattr(circuit, "get_next"):
                        it = circuit.get_next(it)
                    else:
                        it = next(it)
                pos = count + pos
            except Exception:
                pos = position

    try:
        it = circuit.begin()
        for _ in range(pos):
            if hasattr(it, "get_next"):
                it = it.get_next()
            elif hasattr(circuit, "get_next"):
                it = circuit.get_next(it)
            else:
                it = next(it)

        for name in method_names:
            if hasattr(circuit, name):
                try:
                    getattr(circuit, name)(it)
                    return circuit
                except Exception:
                    pass
    except Exception:
        pass

    raise TypeError("Unsupported circuit type for gate removal")

machine.finalize()
