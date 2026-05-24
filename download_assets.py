import re, urllib.request, os

project_dir = "/Users/yoyocubano/Documents/ANTIGRAVITY_CORE_DO_NOT_DELETE/projects/cosmopolita"
assets_dir = os.path.join(project_dir, "assets")
html_path = os.path.join(project_dir, "index.html")

os.makedirs(assets_dir, exist_ok=True)

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Find all image tags
img_pattern = r"<img[^>]*src=[\"'](https://lh3\.googleusercontent\.com/[^\"']+)[\"'][^>]*>"
urls = re.findall(img_pattern, html)

count = 1
for url in set(urls):
    filename = f"image_{count}.jpg"
    filepath = os.path.join(assets_dir, filename)
    try:
        urllib.request.urlretrieve(url, filepath)
        html = html.replace(url, f"./assets/{filename}")
        print(f"Downloaded {filename}")
        count += 1
    except Exception as e:
        print(f"Failed {e}")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
