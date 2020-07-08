import random

class RandomSorter:
    def __init__(self):
        self.CONST_VALID_ANSWER = {
            'positive': ['Y', 'y', 'Yes', 'yes', '네', '예', 'YES'],
            'negative': ['N', 'n', 'No', 'no', '아니오', '아니요', 'NO'],
            'randommode': ['랜덤', '랜덤모드'],
            'normalmode': ['일반', '일반모드']
        }
        self.enable = False
        self.approve = False

    def askEnable(self):
        while True:
            ans = input('모드를 설정합니다.\n랜덤 모드 or 일반 모드\n')
            if ans in self.CONST_VALID_ANSWER['randommode']:
                self.enable = True
                break
            elif ans in self.CONST_VALID_ANSWER['normalmode']:
                self.enable = False
                break
            else:
                print("다시 입력하여 주십시오.")

    def checkSort(self, slist):
        assert isinstance(slist,list)
        # self.approve = False if self.enable else True

        while True:
            print(slist)
            ans = input('분류기준이 다음과 같이 지정되었습니다.\n'
                                          '계속 진행하시겠습니까?(Y/N)\n')
            if ans in self.CONST_VALID_ANSWER['positive']:
                self.approve = True
                break
            elif ans in self.CONST_VALID_ANSWER['negative']:
                self.approve = False
                break
            else:
                print("다시 입력하여 주십시오.")

    def shufflelist(self, slist):
        assert isinstance(slist,list)
        return random.shuffle(slist)

    def isEnable(self):
        return self.enable

    def isApprove(self):
        return self.approve