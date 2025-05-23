import re
import os
import shutil

from blocks import markdown_to_html_node


def print_dir(path_to_dir):
    print(path_to_dir)

    def list_inside(path, indent='-- '):
        for node in os.listdir(path):
            src = os.path.join(path, node)
            print(indent + node)
            if os.path.isdir(src):
                list_inside(f'{src}/', f'{indent}-- ')
    
    list_inside(path_to_dir)

# care when setting force=True, if folder with dest_path exists it will be deleted without warning
def copy_dir(src_path, dest_path, forced=False):
    if not os.path.exists(src_path):
        raise Exception('given source folder does not exist')
    
    if os.path.exists(dest_path):
        if not forced:
            print(f'Called function will delete everything inside ./{dest_path}/\n')
            print_dir(dest_path)
            check = input("\nPress 'y' to proceed...   ")
            if check != 'y': # any input but 'y' stops the execution
                return False
        # removes folder at dest_path and everything inside it
        print(f'Removing all files from ./{dest_path}')
        shutil.rmtree(dest_path)
    
    os.mkdir(dest_path)
    # copies everything from src_path to a recreated folder at dest_path
    print(f'Copying files from ./{src_path} to ./{dest_path}\n')
    def inner_copy(path):
        for node in os.listdir(path):
            src = os.path.join(path, node)
            dest = swap_root_dir(src, dest_path)
            if os.path.isfile(src):
                shutil.copy(src, dest)
            if os.path.isdir(src):
                os.mkdir(dest)
                inner_copy(src)

    inner_copy(src_path) # simply calls the recursive part of a function
    # returns True when executed and False when canceled
    return True

# switch_root('old_root/dir/file', 'new_root') => 'new_root/dir/file'
def swap_root_dir(old_file_path, new_root):
    return f'{new_root}/{old_file_path.partition('/')[2]}'

def extract_title(markdown):
    # splits markdown into lines then looks for one beggining with '# '
    for line in markdown.split('\n'):
        match = re.match(r'^\s*#\s+(.*)', line)
        if match:
            return match.group(1)
    raise Exception('given markdown has no title')

# generates a folder structure using recursion and generate_page functionality
def generate_filesystem(content_root_path, template_path, dest_root_path, basepath):

    # generates a page at generated_path using markdown file at source_path and template at template_path
    def generate_page(source_path, template_path, generated_path):
        if not os.path.isfile(source_path):
            raise FileNotFoundError(f"markdown file not found: {source_path}")
        if not os.path.isfile(template_path):
            raise FileNotFoundError(f"template file not found: {template_path}")
        
        print(f'Generating page from source ./{source_path}')

        with open(source_path, 'r', encoding='utf-8') as md_file:
            markdown = md_file.read()
        with open(template_path, 'r', encoding='utf-8') as tpl_file:
            template = tpl_file.read()

        title = extract_title(markdown)
        template = template.replace('{{ Title }}', title)
        content = markdown_to_html_node(markdown).to_html()
        template = template.replace('{{ Content }}', content)
        if basepath != '/': # adjusts links in html for GitHub use
            template = template.replace('href="/', f'href="{basepath}')
            template = template.replace('src="/', f'href="{basepath}')

        dest_dir = os.path.dirname(generated_path)
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)

        with open(generated_path, 'w', encoding='utf-8') as dest_file:
            dest_file.write(template)   

    # generates every directory inside a given folder
    def generate_level(content_dir_path):
        for node in os.listdir(content_dir_path):
            node_path = f'{content_dir_path}/{node}'
            dest_path = node_path.replace(content_root_path, dest_root_path)
            
            if node_path.endswith('.md'): # looks for a markdown file and then converts it to html using generate_page
                    generate_page(node_path, template_path, dest_path.replace('.md', '.html'))

            if os.path.isdir(node_path):
                if os.listdir(node_path): # only tries to recreate non empty folders
                    generate_level(node_path)
                else:
                    os.mkdir(dest_path)

    print(f'Newly generated pages will be placed in ./{dest_root_path}')
    print('=========================================================')
    return generate_level(content_root_path)
