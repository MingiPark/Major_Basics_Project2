import os
import re
import shutil

class FileMoverToRoot(object):

    def __init__(self, rp):
        assert isinstance(rp, str)
        self.__CONST_ROOT_PATH = rp
        # 구조: key : 원 파일이름 value: 라벨의 정수 값들의 대한 리스트
        self.__parsedFileNameDict = dict()
        self.__CONST_LABEL_EXP = '(((\([0-9]+\))(\..*)?))$'
        self.__CONST_EXT_EXP = '(\.[^.]+)$'

    # 라벨을 가지고 있는가?
    def __hasLabel(self, fn):
        assert isinstance(fn, str)
        p = re.compile(self.__CONST_LABEL_EXP)
        ps = p.search(fn)
        if ps is not None and ps.group(3):
            #print('hasLabel called', p.search(fn).group(3))
            return True
        else:
            #print('hasLabel return false')
            return False

    # 라벨 안에 있는 숫자의 위치 반환
    # 괄호 안에 들어가는 숫자 위치 포함, 닫히는 괄호 위치 까지 포함
    def __findLabelNumPos(self, fn):
        assert isinstance(fn, str)
        p = re.compile(self.__CONST_LABEL_EXP)
        s = p.search(fn)
        if s is not None:
            # print('findLabelNumPos called', s.group(3))
            return p.search(fn).start(3) + 1, p.search(fn).end(3) - 1
        else:
            # print('findLabelNumPos return none')
            return None, None

    # 라벨에서 정수 값을 반환
    def __getLabelNum(self, fn):
        assert isinstance(fn, str)
        if self.__hasLabel(fn):
            lbns, lbne = self.__findLabelNumPos(fn)
            return int(fn[lbns:lbne])
        else:
            return None

    # 확장자의 위치를 반환
    def __findExtPos(self, fn):
        assert isinstance(fn, str)
        p = re.compile(self.__CONST_EXT_EXP)
        s = p.search(fn)
        # print('findExtPos called', s)
        if s is not None:
            return p.search(fn).start()
        else:
            return None

    # 파일 명에 확장자가 존재하는가?
    def __hasExt(self, fn):
        assert isinstance(fn, str)
        p = re.compile(self.__CONST_EXT_EXP)
        s = p.search(fn)
        if s is None:
            return False
        else:
            return True

    # 파일 확장자 추출기
    def __extractExt(self, fn):
        assert isinstance(fn, str)
        if self.__hasExt(fn):
            # return os.path.splitext(fn)[-1]
            return fn[self.__findExtPos(fn):]
        else: return ''

    # 라벨을 제거한 이름 출력기
    def __uniqFileNameParser(self, fn):
        assert isinstance(fn, str)
        if not self.__hasLabel(fn):
            return fn
        else:
            lbStartPos, lbEndPos = self.__findLabelNumPos(fn)
            # print('uniqFileNameParser', fn[:lbStartPos - 1] + fn[lbEndPos + 1:])
            return fn[:lbStartPos - 1] + fn[lbEndPos + 1:]

    # 파싱된 파일명이 중복되는가?
    def __isDuplicatedName(self, pfn):
        # self.__parsedFileNameDict = ['a','a.txt']
        assert isinstance(pfn, str)
        if pfn in self.__parsedFileNameDict:
            return True
        else:
            return False

    # ===========알고리즘==================
    # 1. 루트 경로인가?
    #     1.1 (Y) 기억만 한다.
    #     1.2 (N) 파일 이름이 중복 되는가?
    #         1.2.1 (Y) 라벨이 존재하는가?
    #             1.2.1.1 (Y) 라벨 숫자만 max+1 갱신 뒤 기억
    #             1.2.1.2 (N) max+1 인 라벨을 생성 뒤 기억
    #         1.2.2 (N) 파일을 옮기고, 기억 한다.

    # 파일을 설정된 루트로 이동시킨다
    def moveFilesToRoot(self):
        for (path, dir, files) in os.walk(self.__CONST_ROOT_PATH):
            # 모든 파일에 대하여 파일 이름들은
            for filename in files:
                # 확장자 추출
                ext = self.__extractExt(filename)
                # 규칙: 파일이름(숫자).확장자 는 파일이름.확장자 와 같은 이름으로 간주한다.
                # 라벨을 제거한 파일명을 반환한다.
                parsedFileName = self.__uniqFileNameParser(filename)
                print(parsedFileName, self.__getLabelNum(filename))
                # 1.파일이 루트 경로에 있지 않을 때, (이미 중복 체크가 되어 있으므로)
                # 2.파일 이름 자체가 중복될때,
                if not path == self.__CONST_ROOT_PATH and self.__isDuplicatedName(parsedFileName):
                    # 라벨 위치를 탐색을 시도
                    lbns, lbne = self.__findLabelNumPos(filename)
                    # 지금까지 기억한 라벨 정수 값 중 최대값 + 1
                    lbCnt = max(self.__parsedFileNameDict[parsedFileName]) + 1
                    # 파일 명에 라벨이 존재하지 않으면
                    if lbns is None or lbne is None:
                        # 확장자가 존재하면
                        if self.__hasExt(filename):
                            # 확장자 위치를 고려하여 정수 업데이트
                            extPos = self.__findExtPos(filename)
                            renamedFileName = filename[:extPos] + '(' + str(lbCnt) + ')' + filename[extPos:]
                        # 확장자가 존재하지 않으면
                        else:
                            renamedFileName = filename + '(' + str(lbCnt) + ')'
                    # 파일 명에 라벨이 존재하면
                    # 라벨 안에 정수만 교체하면 된다.
                    elif lbns is not None:
                        renamedFileName = filename[:lbns] + str(lbCnt) + filename[lbne:]

                    # 파일 이름을 변경한다.
                    os.rename(path + '/' + filename, path + '/' + renamedFileName)
                    # 파일을 최상위 디렉토리로 이동
                    shutil.move(path + '/' + renamedFileName, self.__CONST_ROOT_PATH)
                    print('renamedFileName', renamedFileName)
                    # 라벨 값을 기억 한다.
                    assert isinstance(lbCnt, int)
                    self.__parsedFileNameDict[parsedFileName].append(lbCnt)
                else:
                    # 루트가 아닐때, 중복되지 않은 파일명이므로 옮겨도 된다.
                    if not path == self.__CONST_ROOT_PATH:
                        shutil.move(path + '/' + filename, self.__CONST_ROOT_PATH)
                    # 리스트 초기화
                    if parsedFileName not in self.__parsedFileNameDict:
                        print('init')
                        self.__parsedFileNameDict[parsedFileName] = list()
                    # 처음 발견되고 라벨이 장착된 파일이 발견될때
                    if self.__hasLabel(filename):
                        self.__parsedFileNameDict[parsedFileName].append(self.__getLabelNum(filename))
                    else:
                        # 라벨이 안달려 있는 경우는 0으로 취급
                        self.__parsedFileNameDict[parsedFileName].append(0)
                    print('parsedFileNameDict[parsedFileName]', self.__parsedFileNameDict[parsedFileName])

                # debugging
                print('cur list: ', self.__parsedFileNameDict)

                # if ext not in ['jpg', 'png', 'bmp', 'gif']: continue
                print("%s/%s" % (path, filename))
                print(self.__findLabelNumPos(filename))

    # 루트 디렉토리의 자식 폴더들을 삭제
    def deleteFoldersInRoot(self):
        # listdir : 경로에 존재하는 폴더와 파일 출력
        for fdn in os.listdir(self.__CONST_ROOT_PATH):
            # 선택된 객체가 파일이 아닐때,
            if not os.path.isfile(self.__CONST_ROOT_PATH + '/' + fdn):
                # 해당 폴더를 삭제
                shutil.rmtree(self.__CONST_ROOT_PATH + '/' + fdn)
                print('delete dir: ' + self.__CONST_ROOT_PATH + '/' + fdn)


if __name__ == "__main__":
    fmtr = FileMoverToRoot('C:/Users/kdje0/Desktop/pythontest')
    fmtr.moveFilesToRoot()
    fmtr.deleteFoldersInRoot()