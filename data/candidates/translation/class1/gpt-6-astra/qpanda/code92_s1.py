# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT


def calculate_stabilizer_state_info():
    program = QProg()
    program << H(0) << CNOT(0, 1)

    simulator = CPUQVM()
    simulator.run(program, 1)

    sources = [simulator]
    result_method = getattr(simulator, "result", None)
    if callable(result_method):
        sources.insert(0, result_method())

    for source in sources:
        for name in ("get_state_vector", "get_statevector", "get_qstate"):
            getter = getattr(source, name, None)
            if not callable(getter):
                continue
            try:
                state = getter()
            except (TypeError, RuntimeError):
                continue
            if state is None or len(state) != 4:
                continue
            entries = state.items() if isinstance(state, dict) else enumerate(state)
            probabilities = {}
            for basis, amplitude in entries:
                probability = float(abs(amplitude) ** 2)
                if probability > 1e-15:
                    key = basis if isinstance(basis, str) else format(int(basis), "02b")
                    probabilities[key] = probability
            return probabilities

    for source in sources:
        getter = getattr(source, "get_prob_dict", None)
        if callable(getter):
            for arguments in (([0, 1],), ()):
                try:
                    probabilities = getter(*arguments)
                except (TypeError, RuntimeError):
                    continue
                if probabilities:
                    return {
                        key if isinstance(key, str) else format(int(key), "02b"): float(value)
                        for key, value in probabilities.items()
                        if value > 1e-15
                    }

    raise RuntimeError("The simulator did not expose the computed state probabilities.")
