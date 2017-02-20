import os
import imghdr
import time
class ConColor:
    pass

class LogInfo:
    def __init__(self):
        pass

    def error_show(self, error_msg):
        print error_msg
        pass

    def warning_show(self, warning_msg):
        print warning_msg
        pass

    def info_show(self, info_msg):
        print info_msg
        pass
    pass


class FileListSync:
    def __init__(self):
        self.list_file_store_file = 'filelist.log'
        self.list_folder_store_file = 'folderlist.log'
        pass

    def sync_file_list(self, folder_name):
        abs_path_flag = False
        folder_name = os.path.normpath(folder_name)
        if not os.path.isabs(folder_name):
            folder_full_path = os.path.join(os.getcwd(), folder_name)
        else:
            abs_path_flag = True
            folder_full_path = folder_name
        if os.path.isfile(folder_full_path):
            LogInfo().error_show('is a file! %s' % folder_full_path)
            return
        if not os.path.exists(folder_full_path):
            LogInfo().error_show('not exist %s' % folder_full_path)
            return
        list_file_store_file_path = os.path.join(folder_full_path, self.list_file_store_file)
        list_folder_store_file_path = os.path.join(folder_full_path, self.list_folder_store_file)
        scan_result_folders = list()
        base_path_len = len(folder_full_path)
        if os.path.exists(os.path.join(folder_full_path, self.list_file_store_file)):
            log_file_ctime = os.stat(os.path.join(folder_full_path, self.list_file_store_file)).st_mtime
            if os.stat(folder_full_path).st_mtime < log_file_ctime + 300:
                LogInfo().info_show('folder for file-list no need sync %s' % folder_full_path)
                return
            LogInfo().info_show('dir time %d, file time %d' %(os.stat(folder_full_path).st_mtime, log_file_ctime))
        LogInfo().info_show('folder need sync %s' % folder_full_path)
        for (dirpath, dirnames, filenames) in os.walk(folder_full_path, topdown=True):
            tmp_store_file_list_path = os.path.join(dirpath, self.list_file_store_file)
            with open(tmp_store_file_list_path, 'w+') as fd:
                for filename in filenames:
                    if filename != self.list_file_store_file:
                        fd.write(filename + '\n')
            break

    def sync_file_list_recursive(self, folder_name=''):
        folder_name = os.path.normpath(folder_name)
        if not os.path.isabs(folder_name):
            folder_full_path = os.path.join(os.getcwd(), folder_name)
        else:
            folder_full_path = folder_name
        if os.path.isfile(folder_full_path):
            LogInfo().error_show('is a file! %s' % folder_full_path)
            return
        if not os.path.exists(folder_full_path):
            LogInfo().error_show('not exist %s' % folder_full_path)
            return
        if os.path.exists(os.path.join(folder_full_path, self.list_file_store_file)):
            log_file_ctime = os.stat(os.path.join(folder_full_path, self.list_file_store_file)).st_mtime
            if os.stat(folder_full_path).st_mtime < log_file_ctime + 300:
                LogInfo().info_show('folder for file-list no need sync %s' % folder_full_path)
                return
        for (dirpath, dirnames, filenames) in os.walk(folder_full_path, topdown=False):
            for dirname in dirnames:
                dir_path = os.path.join(dirpath, dirname)
                tmp_store_file_list_path = os.path.join(dir_path, self.list_file_store_file)
                log_file_ctime = os.stat(tmp_store_file_list_path).st_mtime
                if os.stat(dir_path).st_mtime <= log_file_ctime:
                    dirnames.remove(dirname)
            tmp_store_file_list_path = os.path.join(dirpath, self.list_file_store_file)
            with open(tmp_store_file_list_path, 'w+') as fd:
                for filename in filenames:
                    if filename != self.list_file_store_file:
                        fd.write(filename + '\n')

    def sync_folder_list(self, folder_name=''):
        abs_path_flag = False
        folder_name = os.path.normpath(folder_name)
        if not os.path.isabs(folder_name):
            folder_full_path = os.path.join(os.getcwd(), folder_name)
        else:
            abs_path_flag = True
            folder_full_path = folder_name
        if os.path.isfile(folder_full_path):
            LogInfo().error_show('is a file! %s' % folder_full_path)
            return
        if not os.path.exists(folder_full_path):
            LogInfo().error_show('not exist %s' % folder_full_path)
            return
        print 'folder scan %s' % folder_full_path
        if os.path.exists(os.path.join(folder_full_path, self.list_folder_store_file)):
            log_file_ctime = os.stat(os.path.join(folder_full_path, self.list_folder_store_file)).st_mtime
            if os.stat(folder_full_path).st_mtime < log_file_ctime + 300:
                LogInfo().info_show('folder for dir-list no need sync %s' % folder_full_path)
                return
        scan_result_folders = list()
        base_path_len = len(folder_full_path)
        for (dirpath, dirnames, filenames) in os.walk(folder_full_path, topdown=False):
            if abs_path_flag:
                scan_result_folders.append(dirpath)
            else:
                scan_result_folders.append(dirpath[base_path_len + 1:])
        tmp_store_folder_list_path = os.path.join(folder_full_path, self.list_folder_store_file)
        with open(tmp_store_folder_list_path, 'w+') as fd:
            for folder_path in scan_result_folders:
                if folder_path != folder_full_path:
                    fd.write(folder_path + '\n')
        pass

    def get_folder_list(self, folder_name, start, end):
        folder_name = os.path.normpath(folder_name)
        if not os.path.isabs(folder_name):
            folder_full_path = os.path.join(os.getcwd(), folder_name)
        else:
            abs_path_flag = True
            folder_full_path = folder_name
        folder_list_store_file = os.path.join(folder_full_path, self.list_folder_store_file)
        if not os.path.exists(folder_list_store_file):
            LogInfo().info_show('folder-list file not exist int %s, do sync first' % folder_name)
            self.sync_folder_list(folder_name)
        tmp_folder_list = list()
        if not os.path.exists(folder_list_store_file):
            LogInfo().error_show('sync failed for folder-list')
            return tmp_folder_list
        with open(folder_list_store_file, 'r') as fd:
            if end == -1:
                for i, line in enumerate(fd):
                    if i >= start:
                        tmp_folder_list.append(line[:-1])
                return tmp_folder_list
            for i, line in enumerate(fd):
                if start <= i <= end:
                    tmp_folder_list.append(line[:-1])
                if i >= end:
                    return tmp_folder_list
        return tmp_folder_list
        pass

    def get_file_list(self, folder_name, start, end):
        folder_name = os.path.normpath(folder_name)
        if not os.path.isabs(folder_name):
            folder_full_path = os.path.join(os.getcwd(), folder_name)
        else:
            abs_path_flag = True
            folder_full_path = folder_name
        file_list_store_file = os.path.join(folder_full_path, self.list_file_store_file)
        if not os.path.exists(file_list_store_file):
            LogInfo().info_show('file-list file not exist int %s, do sync first' % folder_name)
            self.sync_file_list(folder_name)
        tmp_folder_list = list()
        if not os.path.exists(file_list_store_file):
            LogInfo().error_show('sync failed for file-list')
            return tmp_folder_list
        with open(file_list_store_file, 'r') as fd:
            if end == -1:
                for i, line in enumerate(fd):
                    if i >= start:
                        tmp_folder_list.append(line[:-1])
                return tmp_folder_list
            for i, line in enumerate(fd):
                if start <= i <= end:
                    tmp_folder_list.append(line[:-1])
                if i >= end:
                    return tmp_folder_list
        return tmp_folder_list
        pass

if __name__ == '__main__':
    sync_handle = FileListSync()
    start_time = time.time()
    #sync_handle.sync_file_list('./')
    #sync_handle.sync_file_list_recursive(os.getcwd())
    sync_handle.sync_folder_list('static')
    print 'time use %f' % (time.time() - start_time)
    #print sync_handle.get_folder_list('./', 0, 10)
    #print sync_handle.get_file_list('./', 0, 10)
    pass































