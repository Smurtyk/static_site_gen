import sys

from generator import copy_dir, generate_filesystem


SOURCE = 'static'
MARKDOWN = 'content'
TEMPLATE = 'template.html'
DEST_PATH = 'docs'


def main(basepath='/'):
    # copy_dir removes everything from DEST_PATH every time it executes
    # it gives no warning before deletion when forced is set to True
    if copy_dir(SOURCE, DEST_PATH, forced=True): # returns True if it finishes execution
        generate_filesystem(MARKDOWN, TEMPLATE, DEST_PATH, basepath)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
