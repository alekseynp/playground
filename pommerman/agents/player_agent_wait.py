import time

from . import BaseAgent
from .. import characters


class PlayerAgentWait(BaseAgent):
    """The Player Agent that lets the user control a character and waits for input at every timestep"""

    def __init__(self, character=characters.Bomber, agent_control='arrows'):
        super(PlayerAgentWait, self).__init__(character)

        ##
        # @NOTE: DO NOT move this import outside the constructor. It will
        # not work in headless environments like a Docker container
        # and prevents Pommerman from running.
        #
        from pynput import keyboard
        self.keyboard = keyboard
        CONTROLS = {
            'arrows': {
                keyboard.KeyCode.from_char('M'): 0,
                keyboard.Key.up: 1,
                keyboard.Key.down: 2,
                keyboard.Key.left: 3,
                keyboard.Key.right: 4,
                keyboard.Key.space: 5
            },
            'wasd': {
                keyboard.KeyCode.from_char('Q'): 0,
                keyboard.KeyCode.from_char('W'): 1,
                keyboard.KeyCode.from_char('S'): 2,
                keyboard.KeyCode.from_char('A'): 3,
                keyboard.KeyCode.from_char('D'): 4,
                keyboard.KeyCode.from_char('E'): 5
            }
        }

        assert agent_control in CONTROLS, "Unknown control: {}".format(agent_control)
        self._key2act = CONTROLS[agent_control]

        self._keystate = None

    def act(self, obs, action_space):
        with self.keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

        return self._key2act[self._keystate]

    @staticmethod
    def has_user_input():
        return True

    def on_press(self, key):
        self._keystate = key

    def on_release(self, key):
        return False

    def on_key_press(self, k, mod):
        pass
