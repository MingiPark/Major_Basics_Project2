import os
import re
import sys
import glob
path ='C:/'

def searchaction_check():
    loop_flag = True        # 반복 플래그
    result = ''    
    while loop_flag:
        searchactionCheck = input("검색 작업을 진행하시겠습니까?(Y/N) : ")
        listY = ['Y', 'y', 'Yes', 'yes', '네', '예', 'YES']
        listN = ['N', 'n', 'No', 'no', '아니오', '아니요', 'NO']
        enter =""
        
        if searchactionCheck in listY:
            result = 'Y'
            loop_flag = False
        elif searchactionCheck in listN:
            result = 'N'
            loop_flag = False
        # ENTER만 입력했을 때
        elif searchactionCheck is enter:
            print("아래에 나열된 값 중 1개의 값을 입력해주세요.")
            print("검색 작업을 진행할 경우 : {} / 검색 작업을 진행하지 않을 경우 : {}".format(listY, listN))
        # 리스트안에 없는 다른 값 입력했을 때 & 중복값을 입력받았을 때(공백문자 : space, tab만 입력한 경우도 이 곳에 포함)
        elif searchactionCheck not in listY + listN:
            print("잘못된 값을 입력하였습니다. 아래에 나열된 값 중 1개의 값을 입력해주세요.")
            print("검색 작업을 진행할 경우 : {} / 검색 작업을 진행하지 않을 경우 : {}".format(listY, listN))
    return result
        

def startfolder_check():
    loop_flag = True    # 반복 플래그
    result = ''
    while loop_flag:
        folder_name = input("검색을 원하는 작업 폴더를 입력하세요 : ")
        blank_guideline = r"[\s]+"     # 공백 문자 집합의 정규 표현식
        special_char_guideline = r'[/|*"?<>:\\]'    # 특수 문자 집합의 정규 표현식
        p = re.compile(blank_guideline)
        q = re.compile(special_char_guideline)

        # 입력 값에 공백 문자가 없는 경우
        if p.search(folder_name) is None:
            # case 1) 폴더명 길이가 50자를 초과하는 경우
            if (len(folder_name) > 50):
                print("검색할 폴더명 길이는 50자 이내로 하십시오.")
            # case 2) 폴더명에 허용하지 않는 특수문자가 포함된 경우
            elif q.search(folder_name) is not None:
                print('검색할 폴더명에 특수문자 [<,>,|,/,*,",:,?,\]는 포함할 수 없습니다.')
            # case 3) 입력한 폴더명(폴더)가 실제로 존재하지 않는 경우
            elif not(os.path.isdir(path + '/' + str(folder_name))):
                print("입력한 폴더명이 존재하지 않습니다.")
            # case 4) 입력 값이 없는 경우
            elif folder_name == "":
                print("입력 값이 없습니다.")
            # 위의 어떤 case라도 포함되지 않는 경우는 폴더명을 저장 및 폴더명 입력 종료
            else:
                result = folder_name
                loop_flag = False       # 반복 플래그
        
        # 입력 값에 공백 문자가 포함된 경우
        else:
            print("검색 폴더명에 공백 문자(space, tab)가 포함될 수 없습니다.")

    return result  

def file_check():
    loop_flag = True    # 반복 플래그
    result = ''
    while loop_flag:
        file_name = input("검색을 원하는 파일 이름을 입력하세요 : ")
        blank_guideline = r"[\s]+"     # 공백 문자 집합의 정규 표현식
        special_char_guideline = r'[/|*"?<>:\\]'    # 특수 문자 집합의 정규 표현식
        p = re.compile(blank_guideline)
        q = re.compile(special_char_guideline)

        # 입력 값에 공백 문자가 없는 경우
        if not p.match(file_name):
            # case 1) 파일명 길이가 50자를 초과하는 경우
            if (len(file_name) > 50):
                print("검색할 폴더명 길이는 50자 이내로 하십시오.")
            # case 2) 파일명에 허용하지 않는 특수문자가 포함된 경우
            elif q.search(file_name) is not None:
                print('검색할 폴더명에 특수문자 [<,>,|,/,*,",:,?,\]는 포함할 수 없습니다.')
            # case 3) 입력 값이 없는 경우
            elif file_name == "":
                print("입력 값이 없습니다.")
            # 위의 어떤 case라도 포함되지 않는 경우는 폴더명을 저장 및 폴더명 입력 종료
            else:
                result = file_name
                loop_flag = False       # 반복 플래그
        
        # 입력 값에 공백 문자가 포함된 경우
        else:
            print("파일 이름에 공백 문자(space, tab)가 포함될 수 없습니다.")

    return result  

def furthersearch_check():
    loop_flag = True        # 반복 플래그
    result = ''    
    while loop_flag:
        searchactionCheck = input("추가 검색 작업을 진행하시겠습니까?(Y/N) : ")
        listY = ['Y', 'y', 'Yes', 'yes', '네', '예', 'YES']
        listN = ['N', 'n', 'No', 'no', '아니오', '아니요', 'NO']
        enter =""
        
        if searchactionCheck in listY:
            result = 'Y'
            loop_flag = False
        elif searchactionCheck in listN:
            result = 'N'
            loop_flag = False
        # ENTER만 입력했을 때
        elif searchactionCheck is enter:
            print("아래에 나열된 값 중 1개의 값을 입력해주세요.")
            print("추가 검색 작업을 진행할 경우 : {} / 추가 검색 작업을 진행하지 않을 경우 : {}".format(listY, listN))
        # 리스트안에 없는 다른 값 입력했을 때 & 중복값을 입력받았을 때(공백문자 : space, tab만 입력한 경우도 이 곳에 포함)
        elif searchactionCheck not in listY + listN:
            print("잘못된 값을 입력하였습니다. 아래에 나열된 값 중 1개의 값을 입력해주세요.")
            print("추가 검색 작업을 진행할 경우 : {} / 추가 검색 작업을 진행하지 않을 경우 : {}".format(listY, listN))
    return result    

def finder(path):
    os.chdir(path)
    clist = os.listdir(path)
    use = searchaction_check()

    if use == "Y":
        process_flag = True             # 검색 작업 반복 여부를 나타내는 N
        print("검색을 시작합니다...")
        
        while process_flag:
            final_list = list()       # 라벨이 포함된 파일 이름을 저장할 리스트
            file_path_list = list()   # 파일의 절대 경로를 저장할 리스트
            file_name_list = list()   # 파일의 이름만 저장할 리스트(확장자 제외)
            file_dict = dict()        # 파일명을 key, 절대 경로를 value로 저장할 딕셔너리
            
            folder_name = startfolder_check()   # 작업 폴더명 
            paths = path + '/' + folder_name
            abspath_list = glob.glob(paths + '/' + '**', recursive = True)          # 작업 폴더와 서브 폴더에 존재하는 모든 파일과 폴더의 절대 경로을 추출

            # 파일만 따로 리스트에 저장
            for element in abspath_list:
                if (os.path.isfile(element)):
                    replaced_path = element.replace("\\", '/')                      # 절대 경로에서 '\\'을 '/'로 치환
                    file_name = re.split('[.]+', replaced_path.split("/")[-1])[0]   # 정규 표현식을 이용하여 파일 이름만 추출. ex)'C:/Users/user/Desktop/project/test/b/1MB미만/bmp/bmp_test.bmp' -> bmp_test
                    file_name_list.append(file_name)                                # 파일 이름 저장
                    file_path_list.append(replaced_path)                            # 파일 절대 경로 저장
                    file_dict[file_name] = replaced_path                            # 딕셔너리에 이름 및 절대 경로 저장
            
            while True:
                name = file_check()
                replaced_name = re.escape(name)          # 이름에 라벨을 포함하는 파일 검색 시, 정규표현식에서 괄호 ()를 문자 그대로 해석하기 위해, '\'를 붙임.
                guideline = r"^{}(\([0-9]+\))?$".format(replaced_name)
                p = re.compile(guideline)
                for file_name in file_name_list:
                    if p.search(file_name) is not None:         # 파일 이름 리스트의 요소가 입력한 문자열을 포함하는 경우
                        final_list.append(file_name)            # 파일 이름을 최종 리스트에 저장
                    else:
                        pass
                # 입력한 문자열을 포함하는 파일이 존재하지 않는 경우
                if len(final_list) == 0:         
                    print("찾으려는 파일이 존재하지 않습니다.")
                else:
                    break

            # 입력한 문자열을 포함하는 파일이 존재하는 경우
            print("-" * 50 + "<검색 결과>" + "-" * 50)
            for filename in final_list:
                print("파일 이름 : {}, 파일 경로 : {}".format(filename, file_dict[filename]))
            print("-" * 111)
            print('\n')

            mode = furthersearch_check()
            if mode == 'Y':
                pass
            else:
                print("검색을 진행하지 않고 종료합니다.")
                process_flag = False        # 검색 작업 반복 여부를 나타내는 flag = False -> 루프 종료

        # else:
        #     print("존재하지 않는 작업 폴더입니다.")

    elif use == "N":
        print("검색을 진행하지 않고 종료합니다.")

def main():
    finder(path)

if __name__ == "__main__":
    main()
