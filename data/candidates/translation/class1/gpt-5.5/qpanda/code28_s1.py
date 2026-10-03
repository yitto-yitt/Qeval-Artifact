# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq

def visualize_bell_states():
    def _init_machine():
        machine = pq.CPUQVM()
        if hasattr(machine, "init"):
            machine.init()
        elif hasattr(machine, "init_qvm"):
            machine.init_qvm()
        return machine

    def _alloc_many(machine, quantum_count, classical_count):
        if hasattr(machine, "qAlloc_many"):
            qubits = machine.qAlloc_many(quantum_count)
        elif hasattr(machine, "qalloc_many"):
            qubits = machine.qalloc_many(quantum_count)
        else:
            qubits = [machine.qAlloc() for _ in range(quantum_count)]

        if hasattr(machine, "cAlloc_many"):
            cbits = machine.cAlloc_many(classical_count)
        elif hasattr(machine, "calloc_many"):
            cbits = machine.calloc_many(classical_count)
        else:
            cbits = [machine.cAlloc() for _ in range(classical_count)]
        return qubits, cbits

    def _append_measurements(prog, qubits, cbits):
        if hasattr(pq, "measure_all"):
            prog << pq.measure_all(qubits, cbits)
        elif hasattr(pq, "MeasureAll"):
            prog << pq.MeasureAll(qubits, cbits)
        else:
            measure_gate = getattr(pq, "Measure", None) or getattr(pq, "measure")
            for i in range(len(cbits)):
                prog << measure_gate(qubits[i], cbits[i])
        return prog

    def _build_program(kind, qubits, cbits, with_measurements=True):
        prog = pq.QProg()
        if kind == "phi_minus":
            prog << pq.X(qubits[0])
        prog << pq.H(qubits[0])
        prog << pq.CNOT(qubits[0], qubits[1])
        if with_measurements:
            _append_measurements(prog, qubits, cbits)
        return prog

    def _run_distribution(kind):
        machine = _init_machine()
        qubits, cbits = _alloc_many(machine, 2, 2)
        prog = _build_program(kind, qubits, cbits, True)

        if hasattr(machine, "run_with_configuration"):
            result = machine.run_with_configuration(prog, cbits, 1000)
        elif hasattr(machine, "runWithConfiguration"):
            result = machine.runWithConfiguration(prog, cbits, 1000)
        elif hasattr(machine, "prob_run_dict"):
            prog = _build_program(kind, qubits, cbits, False)
            result = machine.prob_run_dict(prog, qubits, -1)
        elif hasattr(machine, "probRunDict"):
            prog = _build_program(kind, qubits, cbits, False)
            result = machine.probRunDict(prog, qubits, -1)
        else:
            prog = _build_program(kind, qubits, cbits, False)
            result = machine.pmeasure(prog, qubits)

        counts = dict(result)
        total = sum(float(v) for v in counts.values())
        return {str(k): float(v) / total for k, v in counts.items() if float(v) != 0.0}

    return {
        "phi_plus": _run_distribution("phi_plus"),
        "phi_minus": _run_distribution("phi_minus"),
    }
