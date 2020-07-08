class SafeMode(object):
    def __init__(self):
        self.CONST_VALID_ANSWER = {
            'positive':['Y' , 'y' , 'Yes' , 'yes' , '네' , '예' , 'YES'],
            'negative':['N' , 'n' , 'No' , 'no' , '아니오' , '아니요' , 'NO'],
            'safemode' : ['안전' , '안전모드'],
            'normalmode' : ['표준', '표준모드']
        }
        self.enable = False
        self.approve = False


    def askEnable(self):
        while True:
            ans = input('모드를 설정합니다.\n표준 모드 or 안전 모드\n')
            if ans in self.CONST_VALID_ANSWER['safemode']:
                self.enable = True
                break
            elif ans in self.CONST_VALID_ANSWER['normalmode']:
                self.enable = False
                break
            else:
                print("다시 입력하여 주십시오.")

    def checkFolderName(self, fn):
        assert isinstance(fn,str)
        # self.approve = False if self.enable else True

        while True:
            ans = input('작업 폴더명이 ' + fn + '과 같이 지정되었습니다.\n'
                                          '계속 진행하시겠습니까?(Y/N)\n')
            if ans in self.CONST_VALID_ANSWER['positive']:
                self.approve = True
                break
            elif ans in self.CONST_VALID_ANSWER['negative']:
                self.approve = False
                break
            else:
                print("다시 입력하여 주십시오.")

    def checkPhotoFile(self):
        # self.approve = False if self.enable else True

        while True:
            ans = input('사진 파일 입력이 완료되었습니다.\n'
                        '다음의 사진 파일로 분류를 진행하시겠습니까?(Y/N)\n')
            if ans in self.CONST_VALID_ANSWER['positive']:
                self.approve = True
                break
            elif ans in self.CONST_VALID_ANSWER['negative']:
                self.approve = False
                break
            else:
                print("다시 입력하여 주십시오.")

    def checkMode(self):
        # self.approve = False if self.enable else True

        while True:
            ans = input('분류 기준을 다음과 같이 선택하셨습니다.\n'
                        '계속 진행하시겠습니까?(Y/N)\n')
            if ans in self.CONST_VALID_ANSWER['positive']:
                self.approve = True
                break
            elif ans in self.CONST_VALID_ANSWER['negative']:
                self.approve = False
                break
            else:
                print("다시 입력하여 주십시오.")

    def isEnable(self):
        return self.enable
    def isApprove(self):
        return self.approve
    def initApprove(self):
        self.approve = False
    def setApprove(self, x):
        assert isinstance(x,bool)
        self.approve = x
