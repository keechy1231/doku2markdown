import re
import os


def convert(infile, outfile):
    with open(infile, "r", encoding="utf-8") as file:
        with open(outfile, "w", encoding="utf-8") as out:

            in_code_block = False

            for line in file:
                if re.fullmatch(r"[\\\s]*", line):
                    continue

                if re.match(r"<code.*?>", line.strip()) or re.match(r"<file.*?>", line.strip()):
                    if in_code_block:
                        out.write("```\n\n")
                    out.write("```\n")
                    in_code_block = True

                    code_content = re.sub(r"<(code|file).*?>", "", line).strip()
                    if code_content:
                        out.write(code_content + "\n")
                    continue

                if line.strip() == "</code>" or line.strip() == "</file>":
                    if in_code_block:
                        out.write("```\n\n")
                        in_code_block = False
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

                elif line.startswith("=="):
                    if in_code_block:
                        out.write("```\n\n")
                        in_code_block = False
                    newline = line.replace("===", "####", 1)
                    newline = newline.replace("=", "").strip()
                    out.write(newline + "\n\n")

                elif "[[" in line:
                    if in_code_block:
                        out.write("```\n\n")
                        in_code_block = False

                    parts = line.split("|", 1)
                    if len(parts) > 1:
                        before_pipe = parts[0]
                        after_pipe = parts[1]
                        if "]]" in after_pipe:
                            after_pipe = "]]"
                        else:
                            after_pipe = ""
                        newline = before_pipe + after_pipe
                    else:
                        newline = line

                    out.write(newline.strip() + "\n\n")

                elif "\t" in line or line.startswith("    "):
                    if not in_code_block:
                        out.write("```\n")
                        in_code_block = True
                    newline = line.lstrip("\t")
                    out.write(newline)

                elif "^" in line:
                    if in_code_block:
                        out.write("```\n\n")
                        in_code_block = False

                    newline = line.replace("^", "|").strip()
                    cols = newline.count("|") - 1
                    table = "|" + "---|" * cols

                    out.write(newline + "\n")
                    out.write(table + "\n")

                elif line.strip().startswith("-"):
                    if in_code_block:
                        out.write("```\n\n")
                        in_code_block = False
                    newline = line.replace("-", "1. ").strip()
                    out.write(newline + "\n")

                elif line.strip().startswith("*"):
                    if in_code_block:
                        out.write("```\n\n")
                        in_code_block = False
                    newline = line.replace("*", "- ").strip()
                    out.write(newline + "\n")

                else:
                    if in_code_block:
                        out.write(line)
                    else:
                        out.write(line)

            if in_code_block:
                out.write("```\n")
        out.close()
    file.close()

def find_all_files():
    input_base = "../pages"
    output_base = "../converted"

    for root, dirs, files in os.walk(input_base):
        for filename in files:
            if filename.endswith(".txt"):
                infile = os.path.join(root, filename)
                new_name = filename.replace(".txt", ".md")

                if not os.path.exists(output_base):
                    os.makedirs(output_base)

                outfile = os.path.join(output_base, new_name)

                convert(infile, outfile)

if __name__ == "__main__":
    find_all_files()