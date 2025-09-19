from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules

# Collect data files, including the 'models' directory inside onnxruntime
datas = collect_data_files('onnxruntime')

# Collect dynamic libraries, this is the most critical part
binaries = collect_dynamic_libs('onnxruntime')

# Add any other missing submodules
hiddenimports = collect_submodules('onnxruntime')