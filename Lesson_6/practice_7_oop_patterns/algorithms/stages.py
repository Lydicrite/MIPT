"""
Состояние (State)
"""

class IPStage():
    def get_stage(self):
        raise NotImplementedError()


class LoadedIPState(IPStage):
    def get_stage(self):
        return 'Init'


class ProcessingIPState(IPStage):
    def get_stage(self):
        return 'Processing'


class FinishedIPState(IPStage):
    def get_stage(self):
        return 'Finished'


class ProcessingSteps(object):
    def __init__(self):
        self._current_state = None
        self._states = self.get_states()

    def get_states(self):
        return [LoadedIPState(), ProcessingIPState(), FinishedIPState()]

    def next_state(self):
        if self._current_state is None:
            self._current_state = self._states[0]
        else:
            index = (self._states.index(self._current_state) + 1) % len(self._states)
            self._current_state = self._states[index]
        return self._current_state

    def info(self):
        state = self.next_state().get_stage()
        return state

if __name__== '__main__':

    proc_stage = ProcessingSteps()
    print([proc_stage.info() for i in range(6)])
