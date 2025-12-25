import os
import re

source_dir = "./original"
output_file = "slides.md"

# Natural sort helper
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

files = [f for f in os.listdir(source_dir) if f.endswith('.html')]
files.sort(key=natural_sort_key)

slides_content = []

# Frontmatter for the whole presentation
header = """---
theme: default
css: ./style.css
highlighter: shiki
lineNumbers: false
aspectRatio: 16/9
canvasWidth: 1280
info: |
  ## 2025 Review
  Presentation slides
drawings:
  persist: false
transition: slide-left
title: 2025 Review
defaults:
  layout: full
---

"""
slides_content.append(header)

for filename in files:
    filepath = os.path.join(source_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Extract the main slide div
        # Looking for <div class="ppt-slide ..."> ... </div>
        # We need to capture the style attribute and the inner content
        
        # Regex to find the opening tag of the ppt-slide div
        match = re.search(r'<div class="ppt-slide([^"]*)"([^>]*)>', content)
        if match:
            classes = match.group(1)
            attributes = match.group(2)
            
            # Extract style from attributes
            style_match = re.search(r'style="([^"]*)"', attributes)
            style = style_match.group(1) if style_match else ""
            
            # Extract inner content
            # We find the start of the div, and then find the corresponding closing div
            start_index = match.end()
            # Simple heuristic: find the last </div> before </body>
            end_match = re.search(r'</div>\s*</body>', content)
            if end_match:
                end_index = end_match.start()
                inner_html = content[start_index:end_index]
            else:
                # Fallback: just take everything until the last </div> found
                last_div = content.rfind('</div>')
                inner_html = content[start_index:last_div]

            # Refactor: Replace fixed height with full height/width for responsiveness
            # The original had h-[720px] w-[1280px] (in style or class)
            # We want the container to fill the Slidev slide area
            
            # Clean up inner HTML indentation
            inner_html = inner_html.strip()

            # Add regex substitutions to replace padding classes
            # inner_html = re.sub(r'py-10', 'py-4', inner_html)
            # inner_html = re.sub(r'py-8', 'py-4', inner_html)
            # inner_html = re.sub(r'p-8', 'p-6', inner_html)
            
            # Generic script extraction
            # Scan for inline <script> tags in the original HTML
            script_section = ""
            script_matches = re.finditer(r'<script([^>]*)>(.*?)</script>', content, re.DOTALL)
            extracted_js = []
            
            for match in script_matches:
                attrs = match.group(1)
                js_code = match.group(2).strip()
                # We only want inline scripts (no src attribute) and non-empty content
                if 'src=' not in attrs and js_code:
                    extracted_js.append(js_code)
            
            if extracted_js:
                combined_js = "\n".join(extracted_js)
                
                # Determine necessary imports
                imports = ["import { onMounted } from 'vue'"]
                if 'new Chart' in combined_js or 'Chart(' in combined_js:
                    imports.append("import Chart from 'chart.js/auto'")
                
                import_block = "\n".join(imports)
                
                # Wrap in onMounted to ensure DOM elements exist
                script_section = f"""
<script setup>
{import_block}

onMounted(() => {{
{combined_js}
}});
</script>
"""

            # Process classes
            # Remove specific fixed dimension classes and ppt-slide
            classes_list = classes.split()
            filtered_classes = []
            for cls in classes_list:
                if cls in ['ppt-slide', 'w-[1280px]', 'h-[720px]', 'min-h-[720px]', 'mx-auto', 'box-border']:
                    continue
                filtered_classes.append(cls)
            
            # Add ensure full size classes
            # We use absolute inset-0 to force the container to fill the slide
            # But we also need to keep the flex properties for layout
            final_classes = " ".join(filtered_classes + ["w-full", "h-full", "absolute", "inset-0"])
            
            # Construct slide markdown
            # We use a wrapper div to hold the background and layout
            slide_md = f"""<!-- Slide: {filename} -->
<div class="{final_classes}" style="{style}">
{inner_html}
</div>
{script_section}

---
"""
            slides_content.append(slide_md)

# Write output
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(slides_content))

print(f"Generated slides.md with {len(files)} slides.")
