"""The hand-off between the two skills: what 3d-print-design writes, x2d-print must read.

Runs the design skill on its two-colour coaster example (with --variants), fills
the job the way x2d-print's SKILL.md says (filament numbers by colour, nozzles from
design.suggested_nozzles), then checks it with x2d-print's own job reader. No Bambu
Studio needed: slicing is tested inside x2d-print with recorded fixtures.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "skills" / "3d-print-design"
X2D = ROOT / "skills" / "x2d-print"
sys.path.insert(0, str(X2D / "scripts"))

import bambu_project as bp  # noqa: E402

# A template as x2d-print reads it: 5 filaments, black is number 5, yellow number 1.
TEMPLATE_COLOURS = {"yellow": 1, "white": 2, "blue": 3, "magenta": 4, "black": 5}
SETTINGS = {
    "filament_settings_id": ["Bambu PLA Basic @BBL X2D"] * 5,
    "filament_type": ["PLA"] * 5,
    "nozzle_diameter": ["0.4", "0.4"],
    "filament_map": ["1"] * 5,
    "layer_height": "0.2",
}


def design_python() -> str:
    venv = DESIGN / ".venv" / "bin" / "python"
    return str(venv) if venv.is_file() else sys.executable


class HandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.project = Path(cls.tmp.name) / "coaster"
        cls.project.mkdir()
        shutil.copy(DESIGN / "examples" / "two-colour-coaster" / "build.py", cls.project / "build.py")
        env = dict(os.environ, PRINT3D_SKILL_DIR=str(DESIGN))
        cls.res = subprocess.run([design_python(), "-P", "build.py", "--variants", "--thin-walls", "0"],
                                 cwd=cls.project, env=env, capture_output=True, text=True, timeout=600)
        cls.job_path = cls.project / "out" / "x2d-job.json"

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def fill(self):
        job = json.loads(self.job_path.read_text())
        job["template"] = "template.3mf"
        for obj in job["objects"]:
            for part in obj["parts"]:
                part["filament"] = TEMPLATE_COLOURS[part["colour"]]
        job["nozzles"] = {str(TEMPLATE_COLOURS[c]): n for c, n in job["design"]["suggested_nozzles"].items()}
        path = self.job_path.with_name("filled.json")
        path.write_text(json.dumps(job))
        return path

    def test_design_build_passes_and_writes_format_2(self):
        self.assertEqual(self.res.returncode, 0, self.res.stdout + self.res.stderr)
        job = json.loads(self.job_path.read_text())
        self.assertEqual(job["design"]["format"], 2)
        self.assertEqual(job["design"]["suggested_nozzles"], {"black": "right", "yellow": "left"})
        self.assertEqual({v["name"] for v in job["variants"]}, {"light", "strong"})
        self.assertIn("| light |", self.res.stdout)

    def test_unfilled_job_is_refused_by_x2d_print(self):
        with self.assertRaises(bp.UserError):
            bp.load_job(self.job_path)

    def test_filled_job_reads_in_x2d_print(self):
        job = bp.load_job(self.fill())
        self.assertEqual([p["filament"] for p in job["objects"][0]["parts"]], [5, 1])
        # black (filament 5) goes right, everything else stays left
        self.assertEqual(bp.nozzle_map(job, SETTINGS), ["1", "1", "1", "1", "2"])
        self.assertEqual(job["settings"]["wall_loops"], "3")

    def test_variants_carry_their_settings(self):
        job = bp.load_job(self.fill())
        by = {v["name"]: bp.variant_job(job, v) for v in job["variants"]}
        self.assertEqual(by["light"]["settings"]["wall_loops"], "2")
        self.assertEqual(by["strong"]["settings"]["sparse_infill_density"], "40%")
        self.assertEqual(by["strong"]["settings"]["layer_height"], "0.2")

    def test_design_and_template_agree(self):
        job = bp.load_job(self.fill())
        warnings = bp.design_warnings(job, dict(SETTINGS, **job["settings"]), bp.nozzle_map(job, SETTINGS))
        self.assertEqual(warnings, [], warnings)


if __name__ == "__main__":
    unittest.main()
