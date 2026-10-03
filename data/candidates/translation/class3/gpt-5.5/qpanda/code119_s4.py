# EVAL_META: task_id=119, framework=qpanda, class=3
import operator
import pyqpanda3.core as pq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = operator.index(num_state_qubits)
    if n < 1:
        raise ValueError("num_state_qubits must be at least 1")
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    if kind == "full":
        total_qubits = 2 * n + 2
    elif kind == "half":
        total_qubits = 2 * n + 2
    else:
        total_qubits = 2 * n + 1

    qvm = None
    if hasattr(pq, "CPUQVM"):
        qvm = pq.CPUQVM()
        for init_name in ("init_qvm", "initQVM", "init"):
            init = getattr(qvm, init_name, None)
            if callable(init):
                try:
                    init()
                    break
                except TypeError:
                    try:
                        init("")
                        break
                    except Exception:
                        pass
                except Exception:
                    pass
    elif hasattr(pq, "init_quantum_machine") and hasattr(pq, "QMachineType"):
        qvm = pq.init_quantum_machine(pq.QMachineType.CPU)

    raw_qubits = None
    if qvm is not None:
        for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            alloc = getattr(qvm, alloc_name, None)
            if callable(alloc):
                raw_qubits = alloc(total_qubits)
                break
    if raw_qubits is None:
        for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            alloc = getattr(pq, alloc_name, None)
            if callable(alloc):
                raw_qubits = alloc(total_qubits)
                break
    if raw_qubits is None:
        raise RuntimeError("Unable to allocate qubits in pyQPanda3")

    qubits = [raw_qubits[i] for i in range(total_qubits)]
    circuit = pq.QCircuit()

    def _insert(gate):
        nonlocal circuit
        if hasattr(circuit, "insert"):
            res = circuit.insert(gate)
            if res is not None:
                circuit = res
        else:
            circuit = circuit << gate

    def _cx(control, target):
        for name in ("CNOT", "CX"):
            fn = getattr(pq, name, None)
            if callable(fn):
                return fn(control, target)
        raise RuntimeError("CNOT/CX gate is not available in pyQPanda3")

    def _ccx(control1, control2, target):
        for name in ("Toffoli", "CCX"):
            fn = getattr(pq, name, None)
            if callable(fn):
                try:
                    return fn(control1, control2, target)
                except TypeError:
                    pass
        x_gate = pq.X(target)
        ctrl_list = [control1, control2]
        if hasattr(x_gate, "control"):
            res = x_gate.control(ctrl_list)
            return res if res is not None else x_gate
        if hasattr(x_gate, "set_control"):
            res = x_gate.set_control(ctrl_list)
            return res if res is not None else x_gate
        raise RuntimeError("Toffoli/controlled-X gate is not available in pyQPanda3")

    def _maj(a, b, c):
        _insert(_cx(a, b))
        _insert(_cx(a, c))
        _insert(_ccx(c, b, a))

    def _uma(a, b, c):
        _insert(_ccx(c, b, a))
        _insert(_cx(a, c))
        _insert(_cx(c, b))

    if kind == "full":
        cin = qubits[0]
        a = qubits[1:1 + n]
        b = qubits[1 + n:1 + 2 * n]
        cout = qubits[1 + 2 * n]
    elif kind == "half":
        a = qubits[0:n]
        b = qubits[n:2 * n]
        cout = qubits[2 * n]
        cin = qubits[2 * n + 1]
    else:
        a = qubits[0:n]
        b = qubits[n:2 * n]
        cin = qubits[2 * n]
        cout = None

    _maj(a[0], b[0], cin)
    for i in range(1, n):
        _maj(a[i], b[i], a[i - 1])

    if cout is not None:
        _insert(_cx(a[n - 1], cout))

    for i in range(n - 1, 0, -1):
        _uma(a[i], b[i], a[i - 1])
    _uma(a[0], b[0], cin)

    create_ripple_carry_adder_circuit._last_qvm = qvm
    create_ripple_carry_adder_circuit._last_qubits = raw_qubits
    return circuit
