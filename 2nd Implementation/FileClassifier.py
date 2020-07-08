import os
import shutil
from FileDataCollector import *
import re
import sys
from datetime import datetime
from FileMoverToRoot import *
# import SafeMode as smo

class FileClassifier(object):
    def __init__(self, rp):
        assert isinstance(rp, str)
        # 작업 폴더 경로 지정
        self.__CONST_ROOT_PATH = rp
        # 2차 분류 기준 딕셔너리 초기화
        # 구조 : key -> {'FILE_NAME', 'CREATED_DATE', 'MODIFIED_DATE'}의 부분 집합
        #         value -> '한글', '영어', '숫자' , '연도', '월' 따위의 문자열
        # self.__second_sort_dict = dict()

        # 분류 기준 폴더 경로 딕셔너리 초기화
        # 구조: key : 집합 {'Root', 'FILE_SIZE', 'FILE_NAME', 'CREATED_DATE', 'MODIFIED_DATE', 'EXTENSION'} 중 단일 혹은 복수의 원소 (Root는 무조건 포함)
        #       value: 리스트 (ex : key가 크기인 경우, [크기 폴더들이 생성된 경로])
        self.__filePathDict = dict()
        self.__filePathDict['Root'] = list()
        self.__filePathDict['Root'].append(os.path.join(rp))

        # 루트 폴더에서 사진 파일과 ETC 파일로 분류
        self.MoveToETC()

    # 한글 문자 판별 함수
    def isHangul(self, text):
        # 파이썬 버전 확인
        pyVer3 = sys.version_info >= (3, 0)

        # 버전이 3.0 이상인 경우
        if pyVer3:
            encText = text
        # 버전이 3.0 미만인 경우
        '''
        else:
            if isinstance(text, unicode):
                encText = text.decode('utf-8')
            else:
                encText = text
        '''
        # 추가 코드 1: text parameter가 str 형식이 아닌 경우, type Error를 발생
        if not isinstance(text, str):
            raise TypeError(text)
        # 범위 : ㄱ-ㅣ가-힣 (자음 또는 모음이 낱으로 존재하는 경우 + 하나의 온전한 글자 형태로 존재하는 경우)
        hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', encText))
        return (hanCount > 0)

    # 파일 확장자 추출기
    def extractExt(self, fn):
        assert isinstance(fn, str)
        return os.path.splitext(fn)[-1]

    # 루트 폴더에서 사진 파일과 아닌 파일을 분리하는 함수
    # 사진 파일이 아닌 파일은 루트 폴더 하위에 ETC 폴더에 삽입된다.
    def MoveToETC(self):
        # ETC 폴더 생성
        etc_path = os.path.join(self.__CONST_ROOT_PATH, 'ETC')
        try:
            if not os.path.exists(etc_path):
                os.makedirs(os.path.join(etc_path))
        except OSError as e:
            print("Failed to create directory {}!".format(etc_path))

        for (path, dir, files) in os.walk(self.__CONST_ROOT_PATH):
            # 모든 파일에 대하여 파일 이름들은
            for filename in files:
                # 확장자 추출
                ext = self.extractExt(filename)
                # 만약 확장자가 {'.bmp', '.gif', '.png', '.jpg', '.jpeg'}에 포함되어 있지 않다면,
                # 수정 코드 1 : jpeg 확장자 추가
                if ext not in ['.bmp', '.gif', '.png', '.jpg', '.jpeg']:
                    # 해당 파일을 ETC 폴더로 이동시킨다.
                    shutil.move(path + '/' + filename, os.path.join(etc_path, filename))

    # 사진 파일의 크기에 따라 폴더를 생성하는 함수
    def createDirBySize(self, path):
        assert isinstance(path, str)
        folder_name_list = ['1MB미만', '1MB이상 4MB미만', '4MB이상']
        # 생성되는 폴더의 경로를 저장하는 리스트
        path_list = list()

        for fdstr in folder_name_list:
            # size_path = os.path.join(path, fdstr)
            size_path = path + '/' + fdstr
            # print(size_path)
            try:
                if not os.path.exists(size_path):
                    os.mkdir(size_path)
                    # os.chmod(size_path, 0o777)
            except OSError as e:
                print("Failed to create directory {}!".format(size_path))
            path_list.append(size_path)
        # print(path_list)
        return path_list

    # 사진 파일 이름의 첫 글자에 따라 폴더를 생성하는 함수
    # 파라미터 : 1) __path : 사진 파일의 첫 번째 글자를 폴더명으로 삼는 폴더들의 부모 경로(상위 디렉토리)
    #            2) mode : 한글, 숫자, 영어 따위를 나타내는 str 객체
    def createDirByName(self, __path, mode):
        # 추가 코드 : __path parameter가 str 형식이 아닐 경우, TypeError를 발생!
        if not isinstance(__path, str):
            raise TypeError(__path)
        # 생성되는 폴더의 경로를 저장하는 리스트
        path_list = list()

        # 추가 코드 2 : mode parameter가 str 형식이 아닌 경우, TypeError를 발생!
        if not isinstance(mode, str):
            raise TypeError(mode)
        # 이름 분류 기준이 한글인 경우
        if mode in ['한글', '한', 'kor', 'korean', 'Korean', 'Kor', 'KOREAN', 'KOR']:
            # 추가 코드 3 : __path parameter 값이 유효하지 않은 경우, OSError를 발생!
            if not os.path.exists(__path):
                raise OSError
            etc_path = __path + '/' + 'ETC'
            # 폴더가 존재하지 않는다면
            if not os.path.exists(etc_path):
                # ETC 폴더 생성
                os.makedirs(etc_path)

            # 파일명의 첫 번째 글자를 저장할 set 자료구조 선언(생성되는 폴더 이름이 중복되는 현상을 방지하기 위함.)
            folder_set = set()
            # 폴더 내에 존재하는 파일 중 확장자가 '.bmp', '.gif', '.png', '.jpg', '.jpeg'인 리스트를 저장
            # 수정 코드 2 : jpeg 확장자 추가
            file_list = os.listdir(__path)
            file_list_py = [file for file in file_list if file.endswith(".bmp") or file.endswith(".gif") or file.endswith(".png") or file.endswith(".jpg")
                                or file.endswith(".jpeg")]

            for file_name in file_list_py:
                # 첫 번째 글자를 추출
                ch = list(file_name)[0]
                # print(ch)
                # 만약 첫 번재 글자가 한글이 아닌 경우
                if not (self.isHangul(ch)):
                    # ETC 폴더로 옮긴다.
                    shutil.move(__path + '/' + file_name, etc_path + '/' + file_name)
                # 첫 번째 글자가 한글인 경우
                else:
                    # 한글 문자를 folder_set에 추가
                    folder_set.add(ch)

            # folder_set, 즉 파일명의 첫 글자인 한글이 저장되어 있는 경우(비어있지 않은 경우)
            if folder_set is not None:
                # folder_set에 존재하는 모든 한글 문자에 대하여
                for element in folder_set:
                    korea_folder_path = __path + '/' + element
                    # folder_set에 포함된 한글 문자를 기준으로 폴더 생성
                    os.makedirs(korea_folder_path)
                    # 생성된 폴더 경로를 리스트에 추가
                    path_list.append(korea_folder_path)

        # 이름 분류 기준이 숫자인 경우
        elif mode in ['숫자', 'num', 'number', 'NUM', 'NUMBER', 'Num', 'Number']:
            # 추가 코드 4 : __path parameter 값이 유효하지 않은 경우 OSError를 발생!
            if not os.path.exists(__path):
                raise OSError
            etc_path = __path + '/' + 'ETC'
            # 폴더가 존재하지 않는다면
            if not os.path.exists(etc_path):
                # ETC 폴더 생성
                os.makedirs(etc_path)

            # 파일명의 첫 번째 글자를 저장할 set 선언
            folder_set = set()
            # 폴더 내에 존재하는 파일 중 확장자가 '.bmp', '.gif', '.png', '.jpg'인 리스트를 저장
            # 수정 코드 3 : jpeg 확장자 추가
            file_list = os.listdir(__path)
            file_list_py = [file for file in file_list if file.endswith(".bmp") or file.endswith(".gif") or file.endswith(".png") or file.endswith(".jpg")
                                or file.endswith(".jpeg")]

            for file_name in file_list_py:
                # 모든 파일명에 대하여 첫 번째 글자를 추출
                ch = list(file_name)[0]
                # 만약 첫 번재 글자가 숫자가 아닌 경우
                if not str.isdigit(ch):
                    # ETC 폴더로 옮긴다.
                    shutil.move(__path + '/' + file_name, etc_path + '/' + file_name)
                    # 첫 번째 글자가 숫자인 경우
                else:
                    # folder_set에 숫자 문자를 저장한다
                    folder_set.add(ch)

            # folder_set, 즉 파일명의 첫 글자인 숫자가 저장되어 있는 경우
            if folder_set is not None:
                # folder_set에 존재하는 모든 숫자에 대하여
                for element in folder_set:
                    digit_folder_path = __path + '/' + element
                    # folder_set에 포함된 숫자를 기준으로 폴더 생성
                    os.makedirs(digit_folder_path)
                    # 생성된 폴더 경로를 리스트에 추가
                    path_list.append(digit_folder_path)

        # 이름 분류 기준이 영문자인 경우
        elif mode in ['영어', '영', 'eng', 'english', 'Eng', 'English', 'ENGLISH', 'ENG']:
            # 추가 코드 5 : __path parameter 값이 유효하지 않은 경우 OSError를 발생!
            if not os.path.exists(__path):
                raise OSError
            etc_path = __path + '/' + 'ETC'
            # 폴더가 존재하지 않는다면
            if not os.path.exists(etc_path):
                # ETC 폴더 생성
                os.makedirs(etc_path)

            # 파일명의 첫 번째 글자를 저장할 리스트 선언
            folder_list = list()
            # 폴더 내에 존재하는 파일 중 확장자가 '.bmp', '.gif', '.png', '.jpg'인 리스트를 저장
            # 코드 수정 4 : jpeg 확장자 추가
            file_list = os.listdir(__path)
            file_list_py = [file for file in file_list if file.endswith(".bmp") or file.endswith(".gif") or file.endswith(".png") or file.endswith(".jpg")
                                or file.endswith(".jpeg")]

            for file_name in file_list_py:
                # 모든 파일명에 대하여 첫 번째 글자를 추출
                ch = list(file_name)[0]
                # 영문자인지 판별하기 위해 정규표현식 패턴 생성
                pattern = "^[a-zA-Z]{1}$"
                p = re.compile(pattern)
                ps = p.search(ch)
                # 만약 첫 번재 글자가 영문자가 아닌 경우
                if ps is None:
                    # ETC 폴더로 옮긴다.
                    shutil.move(__path + '/' + file_name, os.path.join(etc_path, file_name))
                # 첫 번째 글자가 영문자인 경우
                else:
                    # folder_set에 알파벳을 추가
                    folder_list.append(ch)

            # folder_list, 즉 파일명의 첫 번째 알파벳이 저장되어 있는 상태인 경우
            if folder_list is not None:
                # set 자료형을 이용하여, 중복되는 문자 제거
                folder_set = set(folder_list)
                # folder_set에 포함된 첫 번쨰 영문자를 기준으로 폴더 생성(os.makedirs(), os.mkdir()는 대소문자 구분이 없다.)
                for element in folder_set:
                    # 따라서, 첫 번째 영문자가 대문자라면
                    if element.isupper():
                        # 강제로 소문자로 변환
                        element = element.lower()
                    alpha_folder_path = __path + '/' + element
                    # 만들고자 하는 폴더가 존재하지 않을 경우
                    if not os.path.exists(alpha_folder_path):
                        os.makedirs(alpha_folder_path)
                        # 생성된 폴더 경로를 리스트에 추가
                        path_list.append(alpha_folder_path)
                    # 이미 만들고자 하는 폴더가 존재할 경우
                    else:
                        continue
        
        # 추가 코드 : mode parameter가 주어진 범주에 포함되지 않는 경우, AssertionError 메시지를 출력함
        else:
            raise AssertionError(mode)

        # 최종 생성된 폴더의 경로를 저장하는 리스트를 반환
        return path_list

    # 사진 파일의 생성날짜에 따라 폴더를 생성하는 함수
    # 파라미터 : 1) __path : 사진 파일의 첫 번째 글자를 폴더명으로 삼는 폴더들의 부모 경로(상위 디렉토리)
    #            2) mode : 연도, 월 따위를 나타내는 str 객체
    def createDirByCD(self, __path, mode):
        # 추가 코드 : __path parameter가 str 형식이 아닐 경우, TypeError를 발생
        if not isinstance(__path, str):
            raise TypeError(__path)
        # 추가 코드 : __path parameter가 유효한(실제로 존재하는) 값이 아닌 경우, OSError를 발생
        if not os.path.isdir(__path):
            raise OSError(__path)
        # 생성되는 폴더의 경로를 저장하는 리스트
        path_list = list()
        # 생성될 폴더 이름의 형식 변수 초기화
        strf = '\0'
        # ETC 폴더 생성
        etc_path = os.path.join(__path, 'ETC')
        try:
            if not os.path.exists(etc_path):
                os.makedirs(os.path.join(etc_path))
        except OSError as e:
            print("Failed to create directory {}!".format(etc_path))

        # 파일 생성일시를 저장할 set 선언
        folder_set = set()
        # 폴더 내에 존재하는 파일 중 확장자가 '.bmp', '.gif', '.png', '.jpg, '.jpeg'인 리스트를 저장
        # 수정 코드 : jpeg 확장자 추가함
        file_list = os.listdir(__path)
        file_list_py = [file for file in file_list if file.endswith(".bmp") or file.endswith(".gif") or file.endswith(".png") or file.endswith(".jpg")
                            or file.endswith(".jpeg")]

        # 2차 분류 기준이 연도인 경우
        # 추가 코드 : mode parameter가 str 형식이 아닌 경우, TypeError를 발생
        if not isinstance(mode, str):
            raise TypeError(mode)
        if mode in ['년', '년도', 'Y', 'Year', 'y', 'year', 'YEAR']:
            # 폴더 이름 형식은 년도
            strf = '%Y'
        # 2차 분류 기준이 월인 경우
        elif mode in ['월', '달', 'month', 'Month', 'm', 'MONTH', 'M']:
            # 폴더 이름 형식은 월
            strf = '%m'
        # 추가 코드 : mode parameter가 주어진 범주에 포함되지 않는 경우, AssertionError 메시지를 출력함
        else:
            raise AssertionError(mode)

        for file_name in file_list_py:
            # 파일의 절대 경로
            full_path = __path + '/' + file_name
            # 모든 파일에 대해 생성년도 또는 월을 추출
            created_time = datetime.fromtimestamp(os.path.getctime(full_path)).strftime(strf)
            # folder_set에 추가
            folder_set.add(created_time)

        # 생성할 폴더 경로명 초기화
        path = '\0'
        # folder_set에 있는 연도 혹은 월별로 폴더를 생성
        for value in folder_set:
            # 2차 분류 기준이 년도인 경우
            if strf == '%Y':
                path = __path + '/' + value + '년'
            # 2차 분류 기준이 월인 경우
            elif strf == '%m':
                path = __path + '/' + value + '월'
            try:
                if not os.path.exists(path):
                    os.makedirs(path)
            except OSError as e:
                print("Failed to create directory {}!".format(path))

            # path_list에 생성된 폴더 경로를 저장
            path_list.append(path)

        # path_list 반환
        return path_list

    # 사진 파일의 수정날짜에 따라 폴더를 생성하는 함수
    # 파라미터 : 1) __path : 사진 파일의 첫 번째 글자를 폴더명으로 삼는 폴더들의 부모 경로(상위 디렉토리)
    #            2) mode : 연도, 월 따위를 나타내는 str 객체
    def createDirByMD(self, __path, mode):
        # 추가 코드 : __path parameter가 str 형식이 아닐 경우, TypeError 발생
        if not isinstance(__path, str):
            raise TypeError(__path)
        # 추가 코드 : __path parameter가 유효한(실제로 존재하는) 값이 아닌 경우, OSError를 발생
        if not os.path.isdir(__path):
            raise OSError(__path)
        # 생성되는 폴더의 경로를 저장하는 리스트
        path_list = list()
        # 생성될 폴더 이름의 형식 변수 초기화
        strf = '\0'
        # ETC 폴더 생성
        etc_path = os.path.join(__path, 'ETC')
        try:
            if not os.path.exists(etc_path):
                os.makedirs(os.path.join(etc_path))
        except OSError as e:
            print("Failed to create directory {}!".format(etc_path))

        # 파일 수정일시를 저장할 set 선언
        folder_set = set()
        # 폴더 내에 존재하는 파일 중 확장자가 '.bmp', '.gif', '.png', '.jpg'인 리스트를 저장
        # 수정 코드 : jpeg 확장자 추가함
        file_list = os.listdir(__path)
        file_list_py = [file for file in file_list if file.endswith(".bmp") or file.endswith(".gif") or file.endswith(".png") or file.endswith(".jpg")
                            or file.endswith(".jpeg")]

        # 추가 코드 : mode parameter가 str 형식이 아닌 경우, TypeError 발생
        if not isinstance(mode, str):
            raise TypeError(mode)
        # 2차 분류 기준이 연도인 경우
        if mode in ['년', '년도', 'Y', 'Year', 'y', 'year', 'YEAR']:
            # 폴더 이름 형식은 년도
            strf = '%Y'
        # 2차 분류 기준이 월인 경우
        elif mode in ['월', '달', 'month', 'Month', 'm', 'MONTH', 'M']:
            # 폴더 이름 형식은 월
            strf = '%m'
        # 추가 코드 : mode parameter가 주어진 범주에 포함되지 않는 경우, AssertionError 메시지를 출력함
        else:
            raise AssertionError(mode)

        for file_name in file_list_py:
            # 파일의 절대 경로
            full_path = __path + '/' + file_name
            # 모든 파일에 대해 생성년도 또는 월을 추출
            created_time = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime(strf)
            # folder_set에 추가
            folder_set.add(created_time)

        # 생성할 폴더 경로명 초기화
        path = '\0'
        # folder_set에 있는 연도 혹은 월별로 폴더를 생성
        for value in folder_set:
            # 2차 분류 기준이 년도인 경우
            if strf == '%Y':
                path = __path + '/' + value + '년'
            # 2차 분류 기준이 월인 경우
            elif strf == '%m':
                path = __path + '/' + value + '월'
            try:
                if not os.path.exists(path):
                    os.makedirs(path)
            except OSError as e:
                print("Failed to create directory {}!".format(path))

            # path_list에 생성된 폴더 경로를 저장
            path_list.append(path)

        # path_list 반환
        return path_list

    # 사진 파일의 확장자에 따라 폴더를 생성하는 함수
    def createDirByExt(self, path):
        assert isinstance(path, str)
        # 추가 코드 : path parameter가 유효한(실제로 존재하는) 값이 아닌 경우, OSError를 발생
        if not os.path.isdir(path):
            raise OSError(path)
        # 수정 코드 : jpeg 확장자 추가함
        folder_name_list = ['bmp', 'gif', 'png', 'jpg', 'jpeg']
        # 생성되는 폴더의 경로를 저장하는 리스트
        path_list = list()

        for fdstr in folder_name_list:
            ext_path = path + '/' + fdstr
            try:
                if not os.path.exists(ext_path):
                    os.makedirs(os.path.join(ext_path))
            except OSError as e:
                print("Failed to create directory {}!".format(ext_path))
            path_list.append(ext_path)

        return path_list

    # 실제로 파일을 이동시켜주는 함수
    # 파일이름과 근원지를 알아내야 함.
    # 1차 분류 기준이 이름, 생성날짜, 수정날짜인 경우를 대비해 2차 분류 기준도 받아야 함
    def moveFileToSrc(self, srcPath, second_sort_dict):
        # 추가 코드 1: srcPath parameter가 str 형식이 아닌 경우, TypeError를 발생함
        if not isinstance(srcPath, str):
            raise TypeError(srcPath)
        # 추가 코드 2: srcPath parameter가 str 형식이 아닌 경우, OSError를 발생함
        if not os.path.exists(srcPath):
            raise OSError(srcPath)
        # 추가 코드 3: second_sort_dict parameter가 dict 형식이 아닌 경우, TypeError를 발생함
        if not isinstance(second_sort_dict, dict):
            raise TypeError(second_sort_dict)
        # 추가 코드 4: second_sort_dict의 길이가 0이상 3이하의 범위를 벗어난 경우, assertion error를 발생함
        assert (0 <= len(second_sort_dict) <= 3)

        # 작업 폴더에서 모든 사진 파일에 대한 정보를 추출하는 코드
        # FileDataCollector 클래스 객체 생성
        keys = [key for key in self.__filePathDict.keys() if key != 'Root']
        obj = FileDataCollector(srcPath, *keys)
        # 작업 폴더 내부에 존재하는 모든 사진 파일의 정보를 얻는다.
        rootFileInfoDict = obj.getFileData()

         # 실제로 파일을 이동시키는 코드
        # 각각의 파일 경로명에 대하여
        for filepath in rootFileInfoDict.keys():
            # print(filepath)
            # 파일 이름을 추출
            filename = (filepath.split('/'))[-1]
            # print(filename)
            # 리스트를 순회하는 동안 누적될 경로를 저장할 변수 선언
            # 초기 위치: 작업 폴더 경로, 최종 위치 : 실제 파일이 저장될 경로
            workpath = self.__CONST_ROOT_PATH

            # 분류기준 생성 폴더 딕셔너리에 존재하는 각각의 key마다
            for key in keys:
                # 해당 파일 정보에서 key에 대응하는 요소(정보)를 추출
                element = rootFileInfoDict[filepath][key]
                if element is not None:
                    # print(element)
                    # key가 크기인 경우
                    if key == 'FILE_SIZE':
                        # 파일 크기가 1MB 미만인 경우
                        if element < float(1):
                            # 폴더 경로 누적
                            workpath += ('/' + '1MB미만')
                        elif float(1) <= element < float(4):
                            workpath += ('/' + '1MB이상 4MB미만')
                        else:
                            workpath += ('/' + '4MB이상')

                    # key가 이름인 경우
                    elif key == 'FILE_NAME':
                        # 추가 코드 : second_sort_dict['FILE_NAME']이 2차 분류 기준에 속하지 않은 경우, AssertionError 발생함
                        if (second_sort_dict['FILE_NAME'] is None) or (second_sort_dict['FILE_NAME'] not in ['한글', \
                                '한', 'kor', 'korean', 'Korean', 'Kor', 'KOREAN', 'KOR', '영어', '영', 'eng', 'english', \
                                    'Eng', 'English', 'ENGLISH', 'ENG', '숫자', 'num', 'number', 'NUM', 'NUMBER', 'Num', 'Number']):
                            raise AssertionError(second_sort_dict['FILE_NAME'])
                        # 이름의 첫 번째 문자를 추출
                        ch = list(rootFileInfoDict[filepath][key])[0]
                        # 영문자인지 판별하기 위해 정규표현식 패턴 생성
                        pattern = "^[a-zA-Z]{1}$"
                        p = re.compile(pattern)
                        ps = p.search(ch)
                        # 첫 번째 문자가 영문자인 경우
                        if ps is not None:
                            # 첫 글자가 대문자인 경우
                            if ch.isupper():
                                # 강제로 소문자로 변환
                                ch = ch.lower()
                        # 영문자 이외의 종류에 대한 경우는
                        else:
                            # 통과
                            pass
                        # 폴더 경로 누적
                        workpath += ('/' + ch)

                    # key가 생성날짜인 경우
                    elif key == 'CREATED_DATE':
                        # 추가 코드 5: second_sort_dict key value가 str 형식이 아닌경우, TypeError를 발생함
                        if not isinstance(second_sort_dict['CREATED_DATE'], str):
                            raise TypeError(second_sort_dict['CREATED_DATE'])
                        # 2차 분류 기준이 연도인 경우
                        if second_sort_dict['CREATED_DATE'] in ['년', '년도', 'Y', 'Year', 'y', 'year', 'YEAR']:
                            # 연도 추출(format : '2019-10')
                            year = ''.join(list(rootFileInfoDict[filepath][key])[0:4])
                            # 폴더 경로 누적
                            workpath += ('/' + year + '년')
                        # 2차 분류 기준이 월인 경우
                        elif second_sort_dict['CREATED_DATE'] in ['월', '달', 'month', 'Month', 'm', 'MONTH', 'M']:
                            # 월 추출
                            month = ''.join(list(rootFileInfoDict[filepath][key])[5:])
                            # 폴더 경로 누적
                            workpath += ('/' + month + '월')
                        # 추가 코드 : second_sort_dict['CREATED_DATE']가 위 범위에 없을 경우, AssertionError를 발생함
                        else:
                            raise AssertionError(second_sort_dict['CREATED_DATE'])

                    # key가 수정날짜인 경우
                    elif key == 'MODIFIED_DATE':
                        # 추가 코드 5: second_sort_dict key value가 str 형식이 아닌경우, TypeError를 발생함
                        if not isinstance(second_sort_dict['MODIFIED_DATE'], str):
                            raise TypeError(second_sort_dict['MODIFIED_DATE'])
                        # 2차 분류 기준이 연도인 경우
                        if second_sort_dict['MODIFIED_DATE'] in ['년', '년도', 'Y', 'Year', 'y', 'year', 'YEAR']:
                            # 연도 추출(기존 format : '2019-10')
                            year = ''.join(list(rootFileInfoDict[filepath][key])[0:4])
                            # 폴더 경로 누적
                            workpath += ('/' + year + '년')
                        # 2차 분류 기준이 월인 경우
                        elif second_sort_dict['MODIFIED_DATE'] in ['월', '달', 'month', 'Month', 'm', 'MONTH', 'M']:
                            # 월 추출
                            month = ''.join(list(rootFileInfoDict[filepath][key])[5:])
                            # 폴더 경로 누적
                            workpath += ('/' + month + '월')
                        # 추가 코드 : second_sort_dict['MODIFIED_DATE']가 위 범위에 없을 경우, AssertionError를 발생함
                        else:
                            raise AssertionError(second_sort_dict['MODIFIED_DATE'])

                    # key가 확장자인 경우
                    elif key == 'EXTENSION':
                        # 확장자 추출(기존 format : '.jpg')
                        ext = ''.join(list(rootFileInfoDict[filepath][key])[1:])
                        # 폴더 경로 누적
                        workpath += ('/' + ext)

            # 최종 누적된 폴더 경로가 self.__filePathDict의 마지막 key에 해당하는 value(최종 목적지 경로)와 비교한다.
            key_list =[x for x in self.__filePathDict.keys()]


            if str(workpath) in self.__filePathDict[key_list[-1]]:
                # 경로가 실제로 self.__filePathDict에 존재하면 파일을 이동시킨다.
                shutil.move(srcPath + '/' + filename, workpath + '/' + filename)

    # 파일을 분류 기준에 따라 폴더로 이동시키는 함수
    # 파라미터 : 1) first_sort_list : 1차 분류 기준 리스트
    #            2) second_sort_dict : 2차 분류 기준 딕셔너리
    def mainClassifier(self, first_sort_list, second_sort_dict):
         # 추가 코드 1: first_sort_list가 list 형식이 아닌 경우, TypeError를 발생함
        if not isinstance(first_sort_list, list):
            raise TypeError(first_sort_list)
        # 추가 코드 2: second_sort_dict parameter가 dict 형식이 아닌 경우, TypeError를 발생함
        if not isinstance(second_sort_dict, dict):
            raise TypeError(second_sort_dict)
        # 추가 코드 3: first_sort_list의 길이가 0이상 5이하의 범위를 벗어난 경우, assertion error를 발생함
        assert (0 <= len(first_sort_list) <= 5)
        # 추가 코드 4: second_sort_dict의 길이가 0이상 3이하의 범위를 벗어난 경우, assertion error를 발생함
        assert (0 <= len(second_sort_dict) <= 3)
        
        if first_sort_list is not None:
            # 1차 분류 기준 리스트 요소에 따라 폴더를 생성
            for idx in range(len(first_sort_list)):
                # 추가 코드 5 : list의 각 요소가 int 형식이 아닌 경우, TypeError를 발생함
                if not isinstance(first_sort_list[idx], int):
                    raise TypeError(first_sort_list[idx])
                # 1차 분류 기준이 1번(크기)인 경우
                if int(first_sort_list[idx]) == 1:
                    # 첫 번째 인덱스에 해당하므로, 작업 폴더의 자식 폴더로 생성
                    if idx == 0:
                        # 폴더를 생성한 후, 생성된 폴더 경로를 저장하는 리스트를 반환
                        folder_list = self.createDirBySize(self.__CONST_ROOT_PATH)
                        # 생성된 폴더 경로 리스트를 딕셔너리에 추가
                        self.__filePathDict['FILE_SIZE'] = [path for path in [element for element in folder_list]]
                        # 파일 이동
                        self.moveFileToSrc(self.__CONST_ROOT_PATH, second_sort_dict)

                    # 중간 혹은 마지막 인덱스에 해당하므로, 작업 폴더의 자손 폴더로 생성됨.
                    else:
                        # 현재 딕셔너리에 존재하는 모든 키를 리스트로 반환
                        dict_key_list = [x for x in self.__filePathDict.keys()]
                        # 딕셔너리에서 키 FILE_SIZE에 대응하는 list(value)를 초기화
                        self.__filePathDict['FILE_SIZE'] = list()
                        # 딕셔너리에서 이전 키(마지막 키) 값에 속한 모든 폴더 경로에 대하여
                        for subpath in self.__filePathDict[dict_key_list[-1]]:
                            # 크기에 따른 폴더를 생성하고, 폴더 경로 리스트를 반환
                            folder_list = self.createDirBySize(subpath)
                            # 생성된 폴더 경로 리스트를 딕셔너리에 추가
                            for folder_path in folder_list:
                                if folder_path is not None:
                                    # 폴더 경로를 value인 리스트에 저장
                                    self.__filePathDict['FILE_SIZE'].append(folder_path)
                            # 파일 이동
                            self.moveFileToSrc(subpath, second_sort_dict)

                # 1차 분류 기준이 2번(이름)인 경우
                elif int(first_sort_list[idx]) == 2:
                    # second_sort_dict 자료형이 실제로 딕셔너리인 경우만 다음 코드 진행
                    assert isinstance(second_sort_dict, dict)
                    # 인자로 받은 딕셔너리에 자료가 존재하는 경우
                    if second_sort_dict is not None:
                        # 2차 분류 기준 추출
                        mode = second_sort_dict['FILE_NAME']
                        if not isinstance(mode, str):
                            raise TypeError(mode)
                        # 첫 번째 인덱스에 해당하므로, 작업 폴더의 자식 폴더로 생성
                        if idx == 0:
                            # 폴더를 생성한 후, 생성된 폴더 경로를 저장하는 리스트를 반환
                            folder_list = self.createDirByName(self.__CONST_ROOT_PATH, mode)
                            # 생성된 폴더 경로 리스트를 딕셔너리에 추가
                            self.__filePathDict['FILE_NAME'] = folder_list
                            # 파일 이동
                            self.moveFileToSrc(self.__CONST_ROOT_PATH, second_sort_dict)

                        # 중간 혹은 마지막 인덱스에 해당하므로, 작업 폴더의 자손 폴더로 생성됨.
                        else:
                            # 현재 딕셔너리에 존재하는 모든 키를 리스트로 반환
                            dict_key_list = [str(x) for x in self.__filePathDict.keys()]
                            # 딕셔너리에서 키 FILE_NAME에 대응하는 list(value)를 초기화
                            self.__filePathDict['FILE_NAME'] = list()
                            # 딕셔너리에서 이전 키 값에 속한 모든 폴더 경로에 대하여
                            for subpath in self.__filePathDict[dict_key_list[-1]]:
                                # 2차 분류 기준에 따른 폴더를 생성하고, 폴더 경로 리스트를 반환
                                folder_list = self.createDirByName(subpath, mode)
                                # 폴더 경로 리스트에 포함된 모든 폴더 경로에 대하여
                                for folder_path in folder_list:
                                    if folder_path is not None:
                                        # 폴더 경로를 value인 리스트에 저장
                                        self.__filePathDict['FILE_NAME'].append(folder_path)
                                # 파일 이동
                                self.moveFileToSrc(subpath, second_sort_dict)

                # 1차 분류 기준이 3번(생성날짜)인 경우
                elif int(first_sort_list[idx]) == 3:
                    # second_sort_dict 자료형이 실제로 딕셔너리인 경우만 다음 코드 진행
                    assert isinstance(second_sort_dict, dict)
                    # 인자로 받은 딕셔너리에 자료가 존재하는 경우
                    if second_sort_dict is not None:
                        # 2차 분류 기준 추출
                        mode = second_sort_dict['CREATED_DATE']
                        if not isinstance(mode, str):
                            raise TypeError(mode)
                        # 첫 번째 인덱스에 해당하므로, 작업 폴더의 자식 폴더로 생성
                        if idx == 0:
                            # 여기도 파일 이동 코드 작성
                            # 폴더를 생성한 후, 생성된 폴더 경로를 저장하는 리스트를 반환
                            folder_list = self.createDirByCD(self.__CONST_ROOT_PATH, mode)
                            # 생성된 폴더 경로 리스트를 딕셔너리에 추가
                            self.__filePathDict['CREATED_DATE'] = folder_list
                            # 파일 이동
                            self.moveFileToSrc(self.__CONST_ROOT_PATH, second_sort_dict)

                        # 중간 혹은 마지막 인덱스에 해당하므로, 작업 폴더의 자손 폴더로 생성됨.
                        else:
                            # 현재 딕셔너리에 존재하는 모든 키를 리스트로 반환
                            dict_key_list = [x for x in self.__filePathDict.keys()]
                            # 딕셔너리에서 키 CREATED_DATE에 대응하는 list(value)를 초기화
                            self.__filePathDict['CREATED_DATE'] = list()
                            # 파일 이동 코드 작성
                            # 딕셔너리에서 이전 키 값에 속한 모든 폴더 경로에 대하여
                            for subpath in self.__filePathDict[dict_key_list[-1]]:
                                # 2차 분류 기준에 따른 폴더를 생성하고, 폴더 경로 리스트를 반환
                                folder_list = self.createDirByCD(subpath, mode)
                                # 폴더 경로 리스트에 포함된 모든 폴더 경로에 대하여
                                for folder_path in folder_list:
                                    if folder_path is not None:
                                        # 폴더 경로를 value인 리스트에 저장
                                        self.__filePathDict['CREATED_DATE'].append(folder_path)
                                # 파일 이동
                                self.moveFileToSrc(subpath, second_sort_dict)

                # 1차 분류 기준이 4번(수정 날짜)인 경우
                elif int(first_sort_list[idx]) == 4:
                    # second_sort_dict 자료형이 실제로 딕셔너리인 경우만 다음 코드 진행
                    assert isinstance(second_sort_dict, dict)
                    # 인자로 받은 딕셔너리에 자료가 존재하는 경우
                    if second_sort_dict is not None:
                        # 2차 분류 기준 추출
                        mode = second_sort_dict['MODIFIED_DATE']
                        if not isinstance(mode, str):
                            raise TypeError(mode)
                        # 첫 번째 인덱스에 해당하므로, 작업 폴더의 자식 폴더로 생성
                        if idx == 0:
                            # 여기도 파일 이동 코드 작성
                            # 폴더를 생성한 후, 생성된 폴더 경로를 저장하는 리스트를 반환
                            folder_list = self.createDirByMD(self.__CONST_ROOT_PATH, mode)
                            # 생성된 폴더 경로 리스트를 딕셔너리에 추가
                            self.__filePathDict['MODIFIED_DATE'] = folder_list
                            # 파일 이동
                            self.moveFileToSrc(self.__CONST_ROOT_PATH, second_sort_dict)

                        # 중간 혹은 마지막 인덱스에 해당하므로, 작업 폴더의 자손 폴더로 생성됨.
                        else:
                            # 현재 딕셔너리에 존재하는 모든 키를 리스트로 반환
                            dict_key_list = [x for x in self.__filePathDict.keys()]
                            # 딕셔너리에서 키 MODIFIED_DATE에 대응하는 list(value)를 초기화
                            self.__filePathDict['MODIFIED_DATE'] = list()
                            # 파일 이동 코드 작성
                            # 딕셔너리에서 이전 키 값에 속한 모든 폴더 경로에 대하여
                            for subpath in self.__filePathDict[dict_key_list[-1]]:
                                # 2차 분류 기준에 따른 폴더를 생성하고, 폴더 경로 리스트를 반환
                                folder_list = self.createDirByMD(subpath, mode)
                                # 폴더 경로 리스트에 포함된 모든 폴더 경로에 대하여
                                for folder_path in folder_list:
                                    if folder_path is not None:
                                        # 폴더 경로를 value인 리스트에 저장
                                        self.__filePathDict['MODIFIED_DATE'].append(folder_path)
                                # 파일 이동
                                self.moveFileToSrc(subpath, second_sort_dict)

                # 1차 분류 기준이 5번(확장자)인 경우
                elif int(first_sort_list[idx]) == 5:
                    # 첫 번째 인덱스에 해당하므로, 작업 폴더의 자식 폴더로 생성
                    if idx == 0:
                        # 여기도 파일 이동 코드 작성
                        # 폴더를 생성한 후, 생성된 폴더 경로를 저장하는 리스트를 반환
                        folder_list = self.createDirByExt(self.__CONST_ROOT_PATH)
                        # 생성된 폴더 경로 리스트를 딕셔너리에 추가
                        self.__filePathDict['EXTENSION'] = folder_list
                        # 파일 이동
                        self.moveFileToSrc(self.__CONST_ROOT_PATH, second_sort_dict)

                    # 중간 혹은 마지막 인덱스에 해당하므로, 작업 폴더의 자손 폴더로 생성됨.
                    else:
                        # 현재 딕셔너리에 존재하는 모든 키를 리스트로 반환
                        dict_key_list = [x for x in self.__filePathDict.keys()]
                        # 딕셔너리에서 키 EXTENSION에 대응하는 list(value)를 초기화
                        self.__filePathDict['EXTENSION'] = list()
                        # 파일 이동 코드 작성
                        # 딕셔너리에서 이전 키 값에 속한 모든 폴더 경로에 대하여
                        for subpath in self.__filePathDict[dict_key_list[-1]]:
                            # 크기에 따른 폴더를 생성하고, 폴더 경로 리스트를 반환
                            folder_list = self.createDirByExt(subpath)
                            # 폴더 경로 리스트에 포함된 모든 폴더 경로에 대하여
                            for folder_path in folder_list:
                                if folder_path is not None:
                                    # 폴더 경로를 value인 리스트에 저장
                                    self.__filePathDict['EXTENSION'].append(folder_path)
                            # 파일 이동
                            self.moveFileToSrc(subpath, second_sort_dict)

                # 추가코드 : 1차 분류 기준이 유효한 값이 아닐 경우, AssertionError를 발생함
                else:
                    raise AssertionError(first_sort_list[idx])

            # 분류가 완료되었다는 메세지 출력
            print("Complete to sort the files!!!")

if __name__ == '__main__':
    classifier_obj = FileClassifier('D:/project/test')
    # classifier_obj = FileClassifier({"가":"나"})
    # print(classifier_obj.isHangul({"가":"나"}))
    # print(classifier_obj.extractExt({"가":"나"}))
    # classifier_obj.createDirBySize('D:/project1/test3')
    # classifier_obj.createDirBySize(['가','나'])
    # classifier_obj.createDirByName('A','숫자')
    # classifier_obj.createDirByName('D:/project/test', '1+1')
    # classifier_obj.createDirByCD('D:/project/test', '영')
    # classifier_obj.createDirByCD(['가','나'], '월')
    # classifier_obj.createDirByMD('D:/project/test', '1+1')
    # classifier_obj.createDirByMD('A', '월')
    # classifier_obj.createDirByExt('A')
    # classifier_obj.moveFileToSrc(1, {'FILE_NAME' : '영'})
    # classifier_obj.moveFileToSrc('安',{'FILE_NAME':'영'})
    # classifier_obj.moveFileToSrc('D:/project/test',{})
    first_sort_list = [2, 5, 3, 4, 1]
    second_sort_dict = {'FILE_NAME' : '영', 'CREATED_DATE' : "년", 'MODIFIED_DATE' : "월"}
    # second_sort_dict = {'MODIFIED_DATE' : '영', 'CREATED_DATE' : "년", 'MODIFIED_DATE' : "월"}
    classifier_obj.mainClassifier(first_sort_list, second_sort_dict)
    # classifier_obj.mainClassifier([1,2,3], {'CREATED_DATE' : "영어", 'CREATED_DATE' : '월'})


    # 코드 반복 시, 작업 폴더로 모든 파일을 다시 이동시키는 코드
    # fmtr = FileMoverToRoot('D:/project/test')
    # fmtr.moveFilesToRoot()
    # fmtr.deleteFoldersInRoot()
