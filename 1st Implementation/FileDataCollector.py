import os
from datetime import datetime


class FileDataCollector(object):
    def __init__(self, rp, *mode):
        assert isinstance(rp, str)
        self.__CONST_ROOT_PATH = rp
        self.__CONST_MODELIST = ['FILE_SIZE', 'FILE_NAME', 'CREATED_DATE', 'MODIFIED_DATE', 'EXTENSION']
        self.__isVaildMode(mode)
        self.__CONST_MODE = mode
        # '%Y-%m-%d %H:%M:%S' <= 전체 양식
        self.__CONST_YEAR_AND_MONTH_FORM = '%Y-%m'
        self.__fileData = dict(dict())

    def __isVaildMode(self, mds):
        assert isinstance(mds, tuple)
        assert not (len(mds) <= 0 or len(mds) > 5)
        for md in mds:
            assert md in self.__CONST_MODELIST

    def __getFileSize(self, fdir):
        assert isinstance(fdir, str)
        # 기존 assert 문 제거함. 폴더를 만나는 순간 오류를 발생하기 때문!
        if os.path.isfile(fdir):
            return os.path.getsize(fdir) / (1024**2)

    def __getCreatedDate(self, fdir):
        assert isinstance(fdir, str)
        if os.path.isfile(fdir):
            return datetime.fromtimestamp(os.path.getctime(fdir)).strftime(self.__CONST_YEAR_AND_MONTH_FORM)

    def __getModifiedDate(self, fdir):
        assert isinstance(fdir, str)
        if os.path.isfile(fdir):
            return datetime.fromtimestamp(os.path.getmtime(fdir)).strftime(self.__CONST_YEAR_AND_MONTH_FORM)

    def __getExtension(self, fn):
        assert isinstance(fn, str)
        if os.path.isfile(self.__CONST_ROOT_PATH + '/' + fn):
            return os.path.splitext(fn)[-1]

    def __isFile(self, fdir):
        pass

    def getFileData(self):
        for (path, dir, files) in os.walk(self.__CONST_ROOT_PATH):
            # 모든 파일에 대하여 파일 이름들은
            for filename in files:
                # 파일이 사진 파일 확장자를 가지고 있는 경우에만
                if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.gif') or filename.endswith('.bmp') or filename.endswith('.jpeg'):
                    fileDir = self.__CONST_ROOT_PATH + '/' + filename
                    for i in range(len(self.__CONST_MODE)):
                        md = self.__CONST_MODE[i]
                        # print('md: '  + md)
                        if md == 'FILE_SIZE':
                            data = self.__getFileSize(fileDir)
                        elif md == 'FILE_NAME':
                            data = filename
                        elif md == 'CREATED_DATE':
                            data = self.__getCreatedDate(fileDir)
                        elif md == 'MODIFIED_DATE':
                            data = self.__getModifiedDate(fileDir)
                        elif md == 'EXTENSION':
                            data = self.__getExtension(filename)

                        if fileDir not in self.__fileData.keys():
                            self.__fileData[fileDir] = dict()
                        self.__fileData[fileDir][md] = data
        return self.__fileData

    def showFileData(self):
        self.getFileData()
        for key in self.__fileData.keys():
            print('file Dir: ' + key)
            print(self.__fileData[key])


if __name__ == "__main__":
    keys = ['FILE_SIZE', 'FILE_NAME', 'CREATED_DATE', 'MODIFIED_DATE', 'EXTENSION']
    fdc = FileDataCollector('C:/Users/kdje0/Desktop/pythontest', *keys)
    fdc.showFileData()