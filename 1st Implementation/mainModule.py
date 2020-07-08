# -*- coding: utf-8 -*-
import os
import re
import sys
import time
from collections import OrderedDict
from FileClassifier import *
import FileMoverToRoot as fmrModule

#처음 작업 위치는 C드라이브 밑으로 변경한다.
path_dir = 'C:/'
#C드라이브 밑에 모든 파일 및 폴더명을 리스트로 가진다.
fileName_list = os.listdir(path_dir)
fileName = ""
classifier_obj = None
second_sort_dict = {}

#폴더생성 함수
def createfolder(directory):
    os.chdir('C:/')
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating Directory" + directory)

#시작 함수
def start():
    while True:
        isValidFN = False
        while not isValidFN:
            print("작업 폴더명을 입력하여 주십시오 : ",end='')
            fileName = sys.stdin.readline().rstrip()
            Enter = ""
            Space = r"\s+"
            Space_check = re.compile(r"\s+")
            if Space_check.search(fileName):
                print("파일명에 공백이 존재하면 안됩니다")
            else:
                isValidFN = True
        # fileName = input("작업 폴더명을 지정해주세요 : ")
        # print(fileName)
        # Enter = ""
        # Space = r"\s+"
        # Space_check = re.compile(Space)
        # 역슬래쉬 부분에 대한 고찰이 필요하다... 해결
        #if fileName not in fileName_list and len(fileName) <= 50 and all([c not in "\/:.?<>|" for c in fileName]):

        if fileName not in fileName_list and len(fileName) <= 50 \
                and fileName is not Enter and all([c not in r"\/:.?\"<>|*" for c in fileName]):
            createfolder(fileName)
            print("작업 폴더가 " + fileName + " 이라는 이름으로 생성되었습니다.")
            return fileName

        #파일명 중복의 경우
        elif fileName in fileName_list:
            print("파일명이 중복되었습니다. 다시 지정해주세요.\n")

        #파일명이 0이거나 50이상인 경우
        #elif len(fileName) > 50 or len(fileName) == 0:
        #공백에 대한 예외처리 필요...미해결
        elif len(fileName) > 50 or fileName is Enter or Space_check.match(fileName):
            print("파일명 지정은 50자이내 입니다.(파일명 미지정도 불가합니다.) 다시 설정해주세요.\n")

        #파일명에 붙일 수 없는 특수문자를 붙인 경우
        elif [c in r"\/:.?<>\"|*" for c in fileName]:
            print('''{/ , \ , : , . , | , < , > , ?, *,"} 는 파일명에 포함될 수 없습니다. 다시 지정해주세요.\n''')

#분류 작업 선택 전 사진 파일이 작업 폴더에 존재하는지 확인
def photochecker(fileName):
    print("사진파일을 작업 폴더에 넣어주세요.\n")

    myPath = 'C:/' + fileName
    file_list = os.listdir(myPath)
    '''
    file_list_photo = [file for file in file_list if file.endswith(".bmp") or file.endswith(".jpg") or
    file.endswith(".png") or file.endswith(".gif")]
    '''
    file_list_photo = [file for file in file_list if file.endswith(".bmp") or
                       file.endswith(".jpeg") or file.endswith(".jpg") or file.endswith(".png") or file.endswith(".gif")]

    # while file_list_photo is not None:
    ### 수정 시작
    oklist = ['OK', 'ok', 'Ok', 'oK']
    while not file_list_photo:
        print("사진파일 또는 사진 폴더가 작업 폴더에 존재하지 않습니다. 사진 파일 또는 사진 폴더를 넣어주세요.")

        # 중간 멈춤 이후 사진 파일이 작업 폴더에 들어오고 ok sign입력시 다음으로 넘어간다. - 미해결
        isok = False
        print('사진 파일을 넣었으면 ok를 입력하여 주십시오')
        while not isok:
            if input() in oklist:
                isok = True

            else:
                print("['OK', 'ok', 'Ok', 'oK'] 중 하나의 올바른 입력을 해주세요.\n")
        file_list = os.listdir(myPath)
        file_list_photo = [file for file in file_list if file.endswith(".bmp") or
                           file.endswith(".jpeg") or file.endswith(".jpg") or
                           file.endswith(".png") or file.endswith(".gif")]
    print("사진 파일이 확인되었습니다.\n")
    time.sleep(2)
    ## 수정끝




#ok 입력을 두 번 받게 되어 없애기로 하였다.
'''
#사진 파일이 작업 폴더에 존재하는 것을 확인하고 'ok'입력을 받는다.
def okcheck():
    while True:
        okChecker = input("사진 파일이 확인되었습니다. 'OK'를 입력하세요 : ")
        list = ['OK', 'ok', 'Ok', 'oK']

        if okChecker in list:
            print("확인되었습니다.\n")
            break
        else:
            print("['OK', 'ok', 'Ok', 'oK'] 중 하나의 올바른 입력을 해주세요.\n")

'''
#사용자 분류기준 입력
def numchecker():
    #e = "\s*[1-5]{1}\s*"
    #e = r"\s*[1-5]{1}\s*"
    #sub = "(\s*[1-5]{1}\s*) + (,\s*[1-5]{1}\s*){1,4}"
    #sub = r"\s*[1-5]{1}\s*" + r"(,\s*[1-5]{1}\s*){1,4}"

    e = r"\s*[1-5]{1}\s*$"
    sub = r"\s*[1-5]{1}\s*" + r"(,\s*[1-5]{1}\s*){1,4}$"

    check1 = re.compile(e)
    check2 = re.compile(sub)

    while True:
        print("*****분류 기준*****")
        print("1. 파일 크기\n2. 파일 이름\n3. 생성 날짜\n4. 수정 날짜\n5. 확장자\n")
        num = input("분류 기준을 입력하세요(ex>1,2,3) : ")
        if check1.match(num) or check2.match(num):
            number = re.compile(r"\s+")
            num = re.sub(number, '', num)
            number_array = num.split(',')
            number_array = list(map(float, number_array))
             #수정 후 추가한 part
            number_array = list(map(int, number_array))

            if check_duplicate(number_array) is True:
                print("OK")
                for value in number_array:
                    if value is 2:
                        key_value1 = standard_filename()
                        second_sort_dict['FILE_NAME'] = key_value1
                    elif value is 3:
                        key_value2 = date()
                        second_sort_dict['CREATED_DATE'] = key_value2
                    elif value is 4:
                        key_value3 = date()
                        second_sort_dict['MODIFIED_DATE'] = key_value3
                return number_array, second_sort_dict
                break
            else:
                print("올바른 형식의 입력이 아닙니다. 다시 입력하세요.\n")
                continue
        else:
            print("올바른 형식의 입력이 아닙니다. 다시 입력하세요.\n")
            continue



#사용자 선택 중복검사
def check_duplicate(number_array):
    while True:
        number_array_check = list(OrderedDict.fromkeys(number_array))

        if number_array != number_array_check:
            print("중복된 입력입니다. 다시 입력하세요.")
            return False
            continue

        elif number_array == number_array_check:
            return True
            break

 #한글,영어,숫자 기준 분류
def standard_filename():
    print("파일이름으로 분류합니다.\n")
    listK = ["한글", "한", "kor", "korean", "Korean", "Kor", "KOREAN", "KOR"]
    listE = ["영어", "영", "eng", "english", "Eng", "English", "ENGLISH", "ENG"]
    listN = ["숫자", "num", "number", "Number", "Num", "NUM", "NUMBER"]
    enter = ""
    while True:
        ken = input("한글/영어/숫자 中 1개를 선택하세요 : ")
        # 한글을 기준으로 선택했을 때
        if ken in listK:
            print("한글을 기준으로 파일을 분류합니다.\n")
            return ken

        # 알파벳을 기준으로 선택했을 때
        elif ken in listE:
            print("알파벳을 기준으로 파일을 분류합니다.\n")
            return ken

        # 숫자를 기준으로 선택했을 때
        elif ken in listN:
            print("숫자를 기준으로 파일을 분류합니다.\n")
            return ken

        # 아무 입력없이 ENTER만 받을 경우
        elif ken is enter:
            print("값을 입력해주세요")

        # 리스트 이외의 값이나 2개 이상의 기준을 선택할 경우
        elif ken not in listK+listN+listE:
            print("유효한 값이 아닙니다. 혹은 2개 이상의 기준을 입력하셨습니다. 다시 입력해주세요")

###############날짜 분류기준 완료###############
def date():
    print("날짜를 기준으로 분류합니다.")
    listY = ["년", "년도", "Y", "Year", "y", "year", "YEAR"]
    listM = ["월", "달", "M", "Month", "m", "MONTH"]
    enter = ""

    while True:
        date_standard = input("년도 or 월 中 1개를 선택하세요 : ")
        # 년도를 기준으로 선택했을 때
        if date_standard in listY:
            print("년도를 기준으로 파일을 분류합니다.\n")
            return date_standard
            # 파일 분류 함수연결해야함
        # 월을 기준으로 선택했을 때
        elif date_standard in listM:
            print("월을 기준으로 파일을 분류합니다.\n")
            return date_standard
            # 파일 분류 함수연결해야함
        # 분류 기준을 선택하지 않은 상태로 엔터키를 바로 입력한 경우
        elif date_standard is enter:
            print("값을 입력해주세요")

        # 리스트 이외의 다른 값 + 년도,월 기준을 모두 입력한 경우
        elif date_standard not in listY + listM:
            print("유효한 값이 아닙니다. 혹은 기준을 2개 입력하셨습니다. 다시 입력해주세요")
            date_standard = '' #해야되는건지고려대상 초기화 문제



#########추가 작업부분 완료##############
def furtheraction__check():

    listY = ['Y', 'y', 'Yes', 'yes', '네', '예', 'YES']
    listN = ['N', 'n', 'No', 'no', '아니오', '아니요', 'NO']
    enter =""
    while True:
        furtheractionCheck = input("추가 작업을 진행하시겠습니까?(Y/N) : ")
        if furtheractionCheck in listY:
            print("추가 작업을 실행하겠습니다.\n")
            break
        elif furtheractionCheck in listN:
            print("프로그램을 종료하겠습니다.")
            sys.exit()
        # 어떠한 값도 입력하지 않고 ENTER만 입력했을 때
        elif furtheractionCheck is enter:
            print("값을 입력해주세요\n")

        # 리스트안에 없는 다른 값 입력했을 때 & 중복값을 입력받았을 때
        elif furtheractionCheck not in listN + listY:
            print("'Y', 'y', 'Yes', 'yes', '네', '예', 'YES', 'N', 'n'"
                  ", 'No', 'no', '아니오', '아니요', 'NO' 중 1개의 값을 입력해 주세요\n")
            furtheractionCheck=''

def furtheraction__check():

    listY = ['Y', 'y', 'Yes', 'yes', '네', '예', 'YES']
    listN = ['N', 'n', 'No', 'no', '아니오', '아니요', 'NO']
    enter =""
    while True:
        furtheractionCheck = input("추가 작업을 진행하시겠습니까?(Y/N) : ")
        if furtheractionCheck in listY:
            print("추가 작업을 실행하겠습니다.\n")
            break
        elif furtheractionCheck in listN:
            print("프로그램을 종료하겠습니다.")
            sys.exit()
        # 어떠한 값도 입력하지 않고 ENTER만 입력했을 때
        elif furtheractionCheck is enter:
            print("값을 입력해주세요\n")

        # 리스트안에 없는 다른 값 입력했을 때 & 중복값을 입력받았을 때
        elif furtheractionCheck not in listN + listY:
            print("'Y', 'y', 'Yes', 'yes', '네', '예', 'YES', 'N', 'n'"
                  ", 'No', 'no', '아니오', '아니요', 'NO' 중 1개의 값을 입력해 주세요\n")
            furtheractionCheck=''

def main():
    print("########################################")
    print("####  WELCOME TO PHOTO CLASSIFIER  #####")
    print("########################################\n")
    print("작업 폴더를 생성합니다.")
    while True:
        fileName = start()
        photochecker(fileName)
        # okcheck()
        #root폴더로 다 끌어올리는 작업 부분
        fmr = fmrModule.FileMoverToRoot('C:/' + fileName)
        fmr.moveFilesToRoot()
        fmr.deleteFoldersInRoot()
        classifier_obj = FileClassifier('C:/' + fileName)
        number_array, second_sort_dict = numchecker()
        classifier_obj.mainClassifier(number_array, second_sort_dict)
        furtheraction__check()




if __name__ == "__main__":
    main()
