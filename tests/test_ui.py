import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pygame
from vector3 import Vector3
from soil import SoilPlot, SoilState
from rose import Rose, RoseStage
from ui import UI

class TestUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.font.init()
        pygame.display.set_mode((800, 600), pygame.HIDDEN)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.surface = pygame.Surface((800, 600))
        self.font = pygame.font.SysFont(None, 24)
        self.ui = UI(self.surface, self.font)

        self.plot = SoilPlot(index=7, position=Vector3(0,0,0))
        self.plot.transition_to(SoilState.PLANTED_DRY)
        self.rose = Rose(self.plot)
        self.rose.grow() # Sprout

    def test_ui_construction(self):
        self.assertIsNotNone(self.ui)
        self.assertEqual(self.ui.surface, self.surface)
        self.assertEqual(self.ui.font, self.font)

    def test_ui_render_no_crash(self):
        # Render without data
        try:
            self.ui.render()
        except Exception as e:
            self.fail(f"UI render with no data raised an exception: {e}")

        # Render with data
        try:
            self.ui.render(self.plot, self.rose)
        except Exception as e:
            self.fail(f"UI render with data raised an exception: {e}")

    def test_ui_no_mutation(self):
        # Capture state before render
        pre_plot_state = self.plot.state
        pre_rose_stage = self.rose.stage

        self.ui.render(self.plot, self.rose)

        # Verify state is untouched after render
        self.assertEqual(self.plot.state, pre_plot_state)
        self.assertEqual(self.rose.stage, pre_rose_stage)

if __name__ == '__main__':
    unittest.main()
