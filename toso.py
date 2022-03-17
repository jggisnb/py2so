import argparse
import os
import shutil


nan = ""

def Get_allpath_from_dir(dir_path,paths:list,exlude_files,unchanged_files,suffix):
    dirs = os.listdir(dir_path)
    for d in dirs:
        is_init_f = "__init__" in d
        is_not_startp = not d.startswith(".")
        is_in_ef = d in exclude_files
        fnp = os.path.join(dir_path,d)
        is_suffix = fnp.endswith(suffix)
        #is folder
        if is_not_startp and not is_init_f and os.path.isdir(fnp):
            Get_allpath_from_dir(fnp,paths,exlude_files,unchanged_files,suffix)
        #is file
        elif is_not_startp and not is_init_f and os.path.isfile(fnp) and not is_in_ef and is_suffix:
            fn, _ = os.path.splitext(fnp)
            paths.append(fn)
        else:
            if is_not_startp:
                unchanged_files.append(fnp)

def delete_build():
    if os.path.exists("build"):
        shutil.rmtree(os.path.join(os.path.dirname(__file__),"build"))

parser = argparse.ArgumentParser(prog="toso.py")
parser.add_argument("-ifd", "--input_folder")
parser.add_argument("-ef","--exclude_files")
parser.add_argument("-ofd","--output_folder")
parser.add_argument("-suf","--suffix",default=".py")
parser.add_argument("-kcf","--keep_cfile",default="0")
parser.add_argument("-py","--python",default="python")
args = parser.parse_args()
input_folder = args.input_folder.strip()
exclude_files = args.exclude_files.strip().split(",")
while nan in exclude_files:exclude_files.remove(nan)
output_folder = args.output_folder.strip()
suffix = args.suffix.strip()
keep_cfile = int(args.keep_cfile.strip())
python = args.python.strip()

paths = []
unchange_arr = []
Get_allpath_from_dir(input_folder,paths,exclude_files,unchange_arr,suffix)

print("\033[32mHere are all the files to be converted so:\033[0m")
pys = []
for p in paths:
    v = p+".py"
    pys.append(v)
    print(v)
yes = input(f"Total {len(paths)} files,Please enter yes or no to continue:")
if yes.lower().strip() == "yes":
    if len(paths):
        pyxs = []
        for i,p in enumerate(paths):
            tar = p + ".pyx"
            pyxs.append(tar)
            shutil.copy(pys[i],tar)

        delete_build()
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        end_str = "]))"
        py_content = "from distutils.core import setup\nfrom Cython.Build import cythonize\nsetup(ext_modules = cythonize(["
        with open("setup.py","w",encoding="utf-8") as wf:
            for p in pyxs:
                py_content += '"'+p+'",'
            py_content = py_content[:-1]
            py_content += end_str
            wf.write(py_content)
            print("\033[32mPython script created, the content is:\033[0m")
            print(py_content+"\n")
        os.system(f"{python} setup.py build_ext")

        builddirs = os.listdir("build")
        libpath = nan
        for bd in builddirs:
            if bd.startswith("lib."):
                shutil.copytree(os.path.join(os.path.dirname(__file__),"build",bd), output_folder)
                break

        for uc in unchange_arr:
            new_uc = uc.replace(input_folder,nan)
            source = input_folder+new_uc
            target = output_folder+new_uc
            target_dir = os.path.dirname(target)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            shutil.copyfile(source,target)

        if keep_cfile == 0:
            for p in paths:
                os.remove(p+".c")
                os.remove(p+".pyx")
                new_p = output_folder + p.replace(input_folder, nan)
                if os.path.exists(new_p):
                    os.remove(new_p + ".pyx")
        delete_build()

        os.remove("setup.py")
    print("\033[32mPy conversion so completed!\033[0m")
else:
    exit(0)





