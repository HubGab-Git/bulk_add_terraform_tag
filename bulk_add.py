import re
import os

def modify_tf_files(directory, your_tag_pattern, your_tag):
    # Wyrażenie regularne do znalezienia bloków tags, z opcjonalnym użyciem merge
    tag_block_pattern = re.compile(r'(tags\s+=\s(?:merge\s*\()?\s*({[^\}]*\}|\w+\.\w+)(?:\))?)', re.DOTALL)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.tf'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                modified_content = content
                changes_made = False

                for match in tag_block_pattern.finditer(content):
                    tag_block = match.group(2)
                    if not re.search(your_tag_pattern, tag_block):
                        if "{" not in tag_block:
                            modified_tag_block = f'merge(\n{{\n  {your_tag}\n}},\n {tag_block}\n)'
                        else:
                            modified_tag_block = re.sub(r'(\s*\}\s*)$', f'\n  {your_tag} \n\1', tag_block, flags=re.DOTALL)
                        # czy_jest= "\x01" in modified_tag_block
                        # print(czy_jest)
                        modified_tag_block= ''.join(['}' if c == '\x01' else c for c in modified_tag_block])
                        full_match = match.group(1)
                        modified_full_match = full_match.replace(tag_block, modified_tag_block)
                        start, end = match.span(1)
                        modified_content = modified_content[:start] + modified_full_match + modified_content[end:]
                        changes_made = True
                        line_number = content.count('\n', 0, start) + 1
                        print(f"Modified file: {file_path} at line {line_number}")

                if changes_made:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
                else:
                    print(f"No changes needed in file: {file_path}")

# Użyj tej funkcji, podając ścieżkę do katalogu i tag
directory_path = '/Users/hubertgabryel/projects/PG/lambda_json_env'
your_tag_pattern = '\"Environment\"\s+=\s\"test\"'
your_tag = '"Environment" = "test"'
modify_tf_files(directory_path, your_tag_pattern, your_tag)
