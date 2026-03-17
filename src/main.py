import os
import shutil
from markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating path from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    with open(template_path, 'r') as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as f:
        f.write(final_html)

    print(f"Page generated at {dest_path}")


def copy_static_to_public(src="static", dest="public"):
    if os.path.exists(dest):
        print(f"Deleting {dest} directoy...")
        shutil.rmtree(dest)
    
    print(f"Creating {dest} directory...")
    os.mkdir(dest)

    copy_directory_contents(src,dest)

def copy_directory_contents(src, dest):
    items = os.listdir(src)
    
    for item in items:
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            copy_directory_contents(src_path, dest_path)


def main():
    copy_static_to_public()

    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html"
    )

    print("\nWebsite generated!")


if __name__ == "__main__":
     main()
    