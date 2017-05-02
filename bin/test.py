from syncFileList import syncFileListBuilder
import os
syncHandler = syncFileListBuilder(os.getcwd())
syncHandler.syncFolder()
