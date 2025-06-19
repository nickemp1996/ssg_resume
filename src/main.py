import os
import shutil
import sys
from markdown import markdown_to_html_node, extract_title

def read_file_to_string(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File not found at {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def write_string_to_file(string, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(string)
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def remove_all_files(directory):
    """Removes all files within a specified directory, but keeps the directory itself."""

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def copy_files(src, dest):
	filenames = os.listdir(src)
	for filename in filenames:
		file_path = os.path.join(src, filename)
		if os.path.isfile(file_path):
			print(f"{file_path} is a file")
			shutil.copy(file_path, dest)
		else:
			print(f"{file_path} is not a file...\nrecurse")
			head, tail = os.path.split(file_path)
			copy_path = os.path.join(dest, tail)
			if not os.path.exists(copy_path):
				os.mkdir(copy_path)
			copy_files(file_path, copy_path)

def setup(src, dest):
	remove_all_files(dest)
	copy_files(src, dest)

def generate_page(file_path, template_path, dest_file_path, basepath):
	print(f"Generating page from {file_path} to {dest_file_path} using {template_path}")
	try:
		markdown = read_file_to_string(file_path)
	except FileNotFoundError:
		raise FileNotFoundError(f"Error: File not found at {file_path}")
	except Exception as e:
		raise Exception(f"An error occurred: {e}")

	try:
		template = read_file_to_string(template_path)
	except FileNotFoundError:
		raise FileNotFoundError(f"Error: File not found at {template_path}")
	except Exception as e:
		raise Exception(f"An error occurred: {e}")

	html = markdown_to_html_node(markdown).to_html()
	title = extract_title(markdown)

	template = template.replace("{{ Title }}", title)
	template = template.replace("{{ Content }}", html)
	template = template.replace('href="/', f'href="{basepath}')
	template = template.replace('src="/', f'src="{basepath}')

	try:
		write_string_to_file(template, dest_file_path)
	except Exception as e:
		raise Exception(f"An error occurred: {e}")

def generate_page_recursive(from_path, template_path, dest_path, basepath):
	filenames = os.listdir(from_path)
	for filename in filenames:
		if filename != ".DS_Store":
			file_path = os.path.join(from_path, filename)
			if os.path.isfile(file_path):
				if ".md" in filename:
					dest_file_path = os.path.join(dest_path, filename.replace(".md", ".html"))
					generate_page(file_path, template_path, dest_file_path, basepath)
			else:
				head, tail = os.path.split(file_path)
				copy_path = os.path.join(dest_path, tail)
				if not os.path.exists(copy_path):
					os.mkdir(copy_path)
				generate_page_recursive(file_path, template_path, copy_path, basepath)

def main():
	if len(sys.argv) == 1:
		basepath = "/"
	else:
		basepath = sys.argv[1]
	print(basepath)
	setup("static", "docs")
	generate_page_recursive("content/", "template.html", "docs/", basepath)

if __name__ == "__main__":
	main()