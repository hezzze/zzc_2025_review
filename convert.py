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
            inner_html = re.sub(r'py-10', 'py-4', inner_html)
            inner_html = re.sub(r'py-8', 'py-4', inner_html)
            inner_html = re.sub(r'p-8', 'p-6', inner_html)
            
            # Special handling for Slide 17 (Charts)
            script_section = ""
            if filename == "17.html":
                script_section = """
<script setup>
import { onMounted } from 'vue'
import Chart from 'chart.js/auto'

onMounted(() => {
    const lbeCtx = document.getElementById('lbeChart').getContext('2d');
    new Chart(lbeCtx, {
        type: 'line',
        data: {
            labels: ['2023', '2024', '2025', '2026', '2027', '2028'],
            datasets: [{
                label: '市场规模（亿美元）',
                data: [12, 14.5, 17.2, 20.3, 24.1, 28.7],
                borderColor: '#5A7BA7',
                backgroundColor: 'rgba(90, 123, 167, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#5A7BA7',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(90, 123, 167, 0.1)' },
                    ticks: { font: { size: 12 }, color: '#718096' }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 12 }, color: '#718096' }
                }
            }
        }
    });

    const aigcCtx = document.getElementById('aigcChart').getContext('2d');
    new Chart(aigcCtx, {
        type: 'doughnut',
        data: {
            labels: ['视频创意', '图像生成', '文本创作', '音频内容'],
            datasets: [{
                data: [35, 28, 22, 15],
                backgroundColor: [
                    'rgba(90, 123, 167, 0.85)',
                    'rgba(90, 123, 167, 0.65)',
                    'rgba(90, 123, 167, 0.45)',
                    'rgba(90, 123, 167, 0.25)'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { size: 11 },
                        color: '#2D3748',
                        padding: 10,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                }
            }
        }
    });
});
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
