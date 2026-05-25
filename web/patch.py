"""
Splices pygbag's generated Python runtime shebang with the custom branded HTML.
The generated index.html has this structure:
  <html ...><script ...>#<!--
    [Python loader code]
  # --></script><head><!-- [rest of generic HTML] -->
We keep everything up to and including '# --></script>' and replace the rest.
"""
import pathlib

generated = pathlib.Path("build/web/index.html").read_text()
custom    = pathlib.Path("web/page.html").read_text()

marker = "# --></script>"
split  = generated.index(marker) + len(marker)

pathlib.Path("build/web/index.html").write_text(generated[:split] + custom)
print("patch.py: index.html patched successfully")
