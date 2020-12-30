import os, zipfile

class IO_Handler():
    def write_file(self, data: dict, dest_dir: str, file_name: str, flag):
        with open(dest_dir + '/' + file_name, flag) as file:
            for key in data:
                file.write(key + ',' + str(data[key]) + '\n')
        return True

    def zip_file(self, source_dir, dest_dir, zip_name):
        with zipfile.ZipFile(dest_dir + '/' + zip_name, 'w') as zf:
            for root, folders, files in os.walk(source_dir):
                for i in files:
                    file_path = root + '/' + i
                    zf.write(file_path, os.path.basename(file_path))

    def open_zip(self, dest_dir, zip_name):
        with zipfile.ZipFile(dest_dir + '/' + zip_name, 'r') as zf:
            return zf

# ## test
# a = IO_Handler()
# # data = {'Version': 'N1', 'NormalDay': '2018-10-10', 'Holiday': '2018-10-15'}
# fee_name = 'haha.zip'
# source_dir = 'D:/aaaa/temp'
# dest_dir = source_dir + '/' +  fee_name
# a.zip_file(dest_dir, source_dir, fee_name)