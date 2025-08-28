import re


with open("test.txt", "r") as file:
    with open("outfile.md", "w") as out:

        in_code_block = False

        for line in file:

            if re.fullmatch(r"[\\\s]*", line):
                continue 

            elif line.startswith("======"):
                if in_code_block:          
                    out.write("```\n\n")
                    in_code_block = False
                newline = line.replace("======", "#", 1)
                newline = newline.replace("=", "").strip()
                out.write(newline + "\n\n")

            elif line.startswith("====="):
                if in_code_block:        
                    out.write("```\n\n")
                    in_code_block = False
                newline = line.replace("=====", "##", 1)
                newline = newline.replace("=", "").strip()
                out.write("\n---\n")
                out.write(newline + "\n\n")

            elif line.startswith("==="): 
                if in_code_block:        
                    out.write("```\n\n")
                    in_code_block = False
                newline = line.replace("====", "###", 1)
                newline = newline.replace("=", "").strip()
                out.write(newline + "\n\n")

            elif "[[" in line:
                if in_code_block:        
                    out.write("```\n\n")
                    in_code_block = False

                # Find the first '|' and keep everything before it
                parts = line.split("|", 1)          # split at first |
                if len(parts) > 1:
                    # Preserve closing brackets if they exist
                    before_pipe = parts[0]
                    after_pipe = parts[1]
                    if "]]" in after_pipe:
                        after_pipe = "]]"           # keep final brackets
                    else:
                        after_pipe = ""
                    newline = before_pipe + after_pipe
                else:
                    newline = line  # no |, leave as-is

                out.write(newline.strip() + "\n\n")

            elif "\t" in line or line.startswith("    "): 
                if not in_code_block:
                    out.write("```\n") 
                    in_code_block = True
                newline = line.lstrip("\t")
                out.write(newline + "") 

            elif "^" in line:
                if in_code_block:        
                    out.write("```\n\n")
                    in_code_block = False

                newline = line.replace("^", "|").strip()
                cols = newline.count("|") - 1
                table = "|" + "---|" * cols

                out.write(newline + "\n")
                out.write(table + "\n")

            else:
                if in_code_block:
                    out.write("```\n")
                    in_code_block = False
                out.write(line)

        if in_code_block:
            out.write("```\n")