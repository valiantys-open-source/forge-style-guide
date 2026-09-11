import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("md_to_html.py")


class MarkdownConverterTests(unittest.TestCase):
    def convert(self, markdown):
        with tempfile.TemporaryDirectory() as directory:
            working_directory = Path(directory)
            source = working_directory / "input.md"
            source.write_text(markdown, encoding="utf-8")
            subprocess.run(
                ["python3", str(SCRIPT), str(source)],
                cwd=working_directory,
                check=True,
                capture_output=True,
                text=True,
            )
            return (working_directory / "forge_style_guide_snippet.html").read_text(encoding="utf-8")

    def test_preserves_semantic_heading_levels(self):
        output = self.convert("# Guide\n\n## Security\n")

        self.assertIn('<h1 id="guide"', output)
        self.assertIn('<h2 id="security"', output)
        self.assertIn('aria-label="Back to top"', output)
        self.assertIn('href="#forge-style-guide"', output)

    def test_removes_executable_markup_and_unsafe_urls(self):
        output = self.convert(
            '# Guide\n\n<script>alert("unsafe")</script>\n\n'
            '[Unsafe](javascript:alert(1))\n\n'
            '<img src="https://example.com/image.png" onerror="alert(1)">\n'
        )

        self.assertNotIn("<script", output)
        self.assertNotIn("alert", output)
        self.assertNotIn("javascript:", output)
        self.assertNotIn("onerror", output)
        self.assertIn('src="https://example.com/image.png"', output)

    def test_preserves_jsx_source(self):
        output = self.convert("```tsx\n<Button onClick={submit}>Save</Button>\n```\n")

        self.assertIn("&lt;Button onClick={submit}&gt;Save&lt;/Button&gt;", output)
        self.assertNotIn("&lt;style=", output)

    def test_adds_semantic_guidance_colors(self):
        output = self.convert("- **Do:** validate input\n- **Avoid:** trusting input\n")

        self.assertIn('<strong style="color:#216e4e;">Do:</strong>', output)
        self.assertIn('<strong style="color:#ae2a19;">Avoid:</strong>', output)


if __name__ == "__main__":
    unittest.main()
