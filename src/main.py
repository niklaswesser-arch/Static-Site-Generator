import os
import shutil
from markdown import markdown_to_html_node, extract_title
import sys

def generate_page(from_path, template_path, dest_path, basepath="/"):
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

    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as f:
        f.write(final_html)

    print(f"Page generated at {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Content directory does not exist: {dir_path_content}")
    
    items = os.listdir(dir_path_content)
    
    for item in items:
        from_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(from_path):
            if item.endswith('.md'):
                html_filename = item.replace('.md', '.html')
                dest_path = os.path.join(dest_dir_path, html_filename)
                
                generate_page(from_path, template_path, dest_path, basepath)
        else:
            new_dest_dir = os.path.join(dest_dir_path, item)
            
            if not os.path.exists(new_dest_dir):
                os.makedirs(new_dest_dir)
                print(f"Creating directory: {new_dest_dir}")
            
            generate_pages_recursive(from_path, template_path, new_dest_dir, basepath)


def copy_static_to_public(src="static", dest="docs"):
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
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    print(f"Using basepath: {basepath}")
    
    copy_static_to_public(src="static", dest="docs")
    
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="docs", 
        basepath=basepath
    )
    
    print("\nWebsite generated successfully!")


if __name__ == "__main__":
     main()
    